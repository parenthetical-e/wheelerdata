import os

# ----
# Global pathing...
DATAPATH = "/data/data2/meta_accumulate/fh"
ROIPATH = os.path.join(DATAPATH, "roinii")
METAPATH = os.path.join(DATAPATH, "fidl")


def get_subject_dirs():
    return ["fh09", "fh11", "fh13", "fh14", "fh15", "fh17", "fh19", 
            "fh21", "fh23", "fh24", "fh25", "fh26", "fh27", "fh28"]


def get_subject_paths():
    return [os.path.join(DATAPATH, subdir) for subdir in get_subject_dirs()]    


def get_subject_fidl_paths():
    return [os.path.join(subpath, "fidl") for subpath in get_subject_paths()]


def get_nod_subject_names():
    return ["fh009", "fh011", "fh013", "fh014", "fh015", "fh017", "fh019", 
            "fh021", "fh023", "fh024", "fh025", "fh026", "fh027", "fh028"]


def get_roi_data_paths(roi):
    return [
        os.path.join(ROIPATH, roi+"_9.nii.gz"),
        os.path.join(ROIPATH, roi+"_11.nii.gz"),
        os.path.join(ROIPATH, roi+"_13.nii.gz"),
        os.path.join(ROIPATH, roi+"_14.nii.gz"),
        os.path.join(ROIPATH, roi+"_15.nii.gz"),
        os.path.join(ROIPATH, roi+"_17.nii.gz"),
        os.path.join(ROIPATH, roi+"_19.nii.gz"),
        os.path.join(ROIPATH, roi+"_21.nii.gz"),
        os.path.join(ROIPATH, roi+"_23.nii.gz"),
        os.path.join(ROIPATH, roi+"_24.nii.gz"),
        os.path.join(ROIPATH, roi+"_25.nii.gz"),
        os.path.join(ROIPATH, roi+"_26.nii.gz"),
        os.path.join(ROIPATH, roi+"_27.nii.gz"),
        os.path.join(ROIPATH, roi+"_28.nii.gz")]


def get_RT_metadata_paths():
    return [
        os.path.join(METAPATH, "trtime_fh009_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh011_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh013_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh014_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh015_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh017_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh019_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh021_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh023_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh024_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh025_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh026_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh027_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh028_RT_corr_EF.csv")]
        

def get_motor_metadata_paths():
    return [
        os.path.join(METAPATH, "trtime_fh009_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh011_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh013_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh014_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh015_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh017_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh019_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh021_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh023_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh024_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh025_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh026_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh027_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh028_motor_EF.csv")]


def get_noise_metadata_paths():
    return [
        os.path.join(METAPATH, "trtime_fh009_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh011_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh013_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh014_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh015_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh017_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh019_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh021_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh023_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh024_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh025_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh026_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh027_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh028_noise_corr_EF.csv")]



