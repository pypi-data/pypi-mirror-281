<p align="center">
<img src="OCELOT.webp">
</p>

# OCELOT
**diffeOmorphiC rEgistration for voxel-wise anOmaly Tracking**

**A tool to generate cohort specific normative PET/CT images and allow comparison with patient PET/CT images.**

## 🛠 Installation Guide
### Virtual Environment Setup

Creating a virtual environment is highly recommended to avoid any potential conflicts with other Python packages.

- **Windows**:
```bash
python -m venv ocelotz_env
.\ocelotz_env\Scripts\activate
```

- **Linux/Mac**:
```bash
python3 -m venv ocelotz_env
source ocelotz_env/bin/activate
```

### Installing OCELOT

With your virtual environment activated, install OCELOT using pip:

```bash
pip install ocelotz # stable recommended version
```

## 📚 Usage Guide
### Getting started
OCELOT has three modes of operation: stratify, normalize and compare. 
To get an overview of the modes, you can simply do:
```bash
ocelot -h
 ```
To get more information for each mode, you can also do:
```bash
ocelot <mode> -h
 ```
So for example:
```bash
ocelot <stratify> -h
```
This will give you more information on the input parameters of the mode. 

### Stratification
The command structure for stratification is:
```bash
ocelot stratify -dir <directory/of/subject/data>
```
OCELOT will attempt to stratify the given presented subjects in `-dir` based on sex, BMI, age and height, standardize them and copy them into a new directory.

### Template creation
```bash
ocelot normalize -sub-dir <directory/of/stratified/subject/data> -clean-up
```
OCELOT will attempt to normalize all subject in the provided `-sub-dir` and create a NormDB from them, including a reference 
- CT
- PET
- SUV-PET
- STD-SUV-PET

### Subject comparison
```bash
ocelot compare -ref-dir <directory/of/template> -sub-dir <directory/of/stratified/subject/data/to/compare> -clean-up -mask-regions [arms | legs | head]
```
OCELOT will attempt to compare all subjects in the `-sub-dir` to the NormDB in the `-ref-dir`. `-clean-up` is optional and removes all intermediate processing data after OCELOT is done. `-mask-regions` is optional and can be used to ignore regions during comparison.

### Output
OCELOT will generate a folder named `OCELOT` in each directory where the results of each processing pipeline can be found.