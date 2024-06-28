# ------------------------------------------------------ Imports ----------------------------------------------------- #
import os
import subprocess
import SimpleITK
import pydicom
import contextlib
import io
import dicom2nifti
import six
import re
import unicodedata

from ocelotz import system
from ocelotz import image_processing


def remove_accents(filename):
    filename = filename.replace(" ", "_")
    if isinstance(filename, type(six.u(''))):
        unicode_filename = filename
    else:
        unicode_filename = six.u(filename)
    cleaned_filename = unicodedata.normalize('NFKD', unicode_filename).encode('ASCII', 'ignore').decode('ASCII')

    cleaned_filename = re.sub('[^\w\s-]', '', cleaned_filename.strip().lower())
    cleaned_filename = re.sub('[-\s]+', '-', cleaned_filename)

    return cleaned_filename


def predict_nifti_file_stem(input_dicom_directory: str):
    dicom_files = os.listdir(input_dicom_directory)
    reference_dicom_file = pydicom.read_file(os.path.join(input_dicom_directory, dicom_files[0]))

    base_filename = ""
    if 'SeriesNumber' in reference_dicom_file:
        base_filename = remove_accents('%s' % reference_dicom_file.SeriesNumber)
        if 'SeriesDescription' in reference_dicom_file:
            base_filename = remove_accents('%s_%s' % (base_filename, reference_dicom_file.SeriesDescription))
        elif 'SequenceName' in reference_dicom_file:
            base_filename = remove_accents('%s_%s' % (base_filename, reference_dicom_file.SequenceName))
        elif 'ProtocolName' in reference_dicom_file:
            base_filename = remove_accents('%s_%s' % (base_filename, reference_dicom_file.ProtocolName))
    else:
        base_filename = remove_accents(reference_dicom_file.SeriesInstanceUID)

    return base_filename


def to_nifti_2(input_dicom_directory: str, output_nifti_directory: str, output_nifti_filename: str):
    nifti_compression = False
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        dicom2nifti.convert_directory(input_dicom_directory, output_nifti_directory, compression=nifti_compression, reorient=True)

    predicted_nifti_file_stem = predict_nifti_file_stem(input_dicom_directory)
    if nifti_compression:
        predicted_nifti_filename = f"{predicted_nifti_file_stem}.nii.gz"
        output_nifti_filename = f"{output_nifti_filename}.nii.gz"
    else:
        predicted_nifti_filename = f"{predicted_nifti_file_stem}.nii"
        output_nifti_filename = f"{output_nifti_filename}.nii"
    predicted_file_path = os.path.join(output_nifti_directory, predicted_nifti_filename)
    output_nifti_file_path = os.path.join(output_nifti_directory, output_nifti_filename)
    os.rename(predicted_file_path, output_nifti_file_path)


def dcm2niix(input_dicom_directory: str, output_nifti_directory: str, output_nifti_filename: str):
    cmd_to_run: list[str] = [system.DCM2NIIX_PATH,
                             '-z', 'y',
                             '-o', output_nifti_directory,
                             '-f', output_nifti_filename,
                             input_dicom_directory]

    try:
        subprocess.run(cmd_to_run, capture_output=True, check=True)
        os.remove(os.path.join(output_nifti_directory, f'{output_nifti_filename}.json'))
    except subprocess.CalledProcessError:
        to_nifti_2(input_dicom_directory, output_nifti_directory, output_nifti_filename)
        print(f"Error during DICOM to NIFTI conversion using dcm2niix. Using fallback.")


def dicom_to_nifti(dicom_directory: str, nifti_file_path: str):
    nifti_directory, nifti_file_name = os.path.split(nifti_file_path)
    nifti_file_stem = nifti_file_name.split(".", 1)[0]

    dcm2niix(dicom_directory, nifti_directory, nifti_file_stem)


def get_DICOM_PET_parameters(dicom_file_path: str) -> dict:
    """
    Get SUV parameters from dicom tags using pydicom
    :param dicom_file_path: Path to the Dicom file to get the SUV parameters from
    :return: suv_parameters, a dictionary with the SUV parameters (weight in kg, dose in mBq)
    """
    ds = pydicom.dcmread(dicom_file_path)
    suv_parameters = {'weight[kg]': ds.PatientWeight,
                      'total_dose[MBq]': (float(ds.RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose) / 1000000),
                      'AcquisitionDate': int(float(ds.AcquisitionDate)),
                      'AcquisitionTime': int(float(ds.AcquisitionTime)),
                      'StudyTime': int(float(ds.StudyTime)),
                      'SeriesTime': int(float(ds.SeriesTime)),
                      'DecayFactor': float(ds.DecayFactor),
                      'DecayCorrection': ds.DecayCorrection,
                      'RadiopharmaceuticalStartTime': int(float(ds.RadiopharmaceuticalInformationSequence[0].RadiopharmaceuticalStartTime)),
                      'RadionuclideHalfLife': float(ds.RadiopharmaceuticalInformationSequence[0].RadionuclideHalfLife)}
    return suv_parameters


def compute_time_difference(time_1, time_2):
    hours = time_1 // 10000
    minutes = (time_1 % 10000) // 100
    seconds = time_1 % 100
    time1 = hours * 3600 + minutes * 60 + seconds

    hours = time_2 // 10000
    minutes = (time_2 % 10000) // 100
    seconds = time_2 % 100
    time2 = hours * 3600 + minutes * 60 + seconds
    return time2-time1


def compute_corrected_activity(patient_parameters: dict):
    injection_to_scan = compute_time_difference(patient_parameters['RadiopharmaceuticalStartTime'], patient_parameters['SeriesTime'])
    injected_activity = patient_parameters['total_dose[MBq]']
    half_life = patient_parameters['RadionuclideHalfLife']

    decay_corrected_activity = injected_activity * pow(2.0, -(injection_to_scan / half_life))
    print(f"Original activity of {injected_activity} MBq after {injection_to_scan/60} min is {decay_corrected_activity} MBq.")
    return decay_corrected_activity


def convert_bq_to_suv(bq_PET_file_path: str, suv_PET_file_path: str, patient_parameters: dict) -> SimpleITK.Image:
    """
    Convert a becquerel PET image to SUV image
    :param bq_PET_file_path: Path to a becquerel PET image to convert to SUV image (can be NRRD, NIFTI, ANALYZE
    :param suv_PET_file_path: Name of the SUV image to be created (preferably with a path)
    :param patient_parameters: A dictionary with the SUV parameters (weight in kg, dose in mBq)
    """

    patient_weight = patient_parameters["weight[kg]"]
    activity = compute_corrected_activity(patient_parameters)

    suv_denominator = (activity / patient_weight) * 1000  # Units in kBq/mL
    suv_conversion_factor = 1 / suv_denominator
    suv_image = image_processing.scale_image(bq_PET_file_path, suv_conversion_factor, suv_PET_file_path)

    return suv_image


def bq_PET_to_suv_PET(bq_PET_file_path: str, suv_PET_file_path: str, DICOM_PET_directory: str):
    DICOM_PET_files = os.listdir(DICOM_PET_directory)
    DICOM_PET_file_probe = os.path.join(DICOM_PET_directory, DICOM_PET_files[0])
    DICOM_PET_parameters = get_DICOM_PET_parameters(DICOM_PET_file_probe)
    convert_bq_to_suv(bq_PET_file_path, suv_PET_file_path, DICOM_PET_parameters)
