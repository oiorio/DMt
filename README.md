# DMt
DMt simplified models

## General description:

This package implements the running of parallel MG5 + madanalysis

The workflow is the following:

1. Download and install MG5_aMC locally

1.1 Includes installing the 6.5.4 LHAPDF

2. Prepare the conditions for running madanalysis

2.1 prepare a py3 environment 

2.2 edit the installation scripts 

3. Write templates for the 4 configuration cards for madgraph and madanalysis: 

3.1 topology 

3.2 run 

3.3 MA5 

3.4 sfs

4. Run a script (done by "sub_mass_condor.py") that prepares and launches jobs on condor, performing the following actions for a selected model/mass range:

4.1 editing the files in 3.1 - 3.4 to change the mass points and the input/output folders

4.2 check the existence of the events / madanalysis folder or whether the model/mass combination was already successful

4.3 for each of the unsuccesful files: write the condor runner and configuration files (done by "submit_condor.py")

4.4 launch them.

5. Clear the directories of the heavy files (.lhe, .gz, the pythia split run folder). This is done with the "sub_mass_condor.py" as well. 

## 1. Downloading and installing MG5

## 2. Prepare the conditions for installing madanalysis

## 3. Write template configuration cards

## 4. Run the scripts

## 5. Clear the directory