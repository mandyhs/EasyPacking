#!/bin/bash

DEFAULT_ROOT=~/workspace

extract() {

#LOCAL_PREBUILD=~/workspace/prebuild_8313
#CAMERA_SW=~/workspace/icg/vieddrv/Source
#CAMERA_SW=~/workspace/vieddrv-github/w/camerasw/Source
LOCAL_PREBUILD=${DEFAULT_ROOT}/${PREBUILD_DIR}
CAMERA_SW=${DEFAULT_ROOT}/${SRC_DIR}

mkdir -p ${CAMERA_SW}/Camera/Platform/LNL/MFTPlugin/LNL/Intel3AUniversal
mkdir -p ${CAMERA_SW}/Camera/Platform/LNL/MFTPlugin/libsubway/x64/LNL

cd ${LOCAL_PREBUILD}
unzip -o Intel3A_* -d ${CAMERA_SW}/Camera/MFTPlugin
unzip -o LNL_Intel3AUniversal_* -d ${CAMERA_SW}/Camera/Platform/LNL/MFTPlugin/LNL/Intel3AUniversal
unzip -o libburstisp_* -d ${CAMERA_SW}/Camera/MFTPlugin
unzip -o libevcp_* -d ${CAMERA_SW}/Camera/MFTPlugin
unzip -o libface_* -d ${CAMERA_SW}/Camera/MFTPlugin
unzip -o libtnr_* -d ${CAMERA_SW}/Camera/MFTPlugin
unzip -o libexpat_* -d ${CAMERA_SW}/Camera/ISP/css
unzip -o libiacss_* -d ${CAMERA_SW}/Camera/ISP/css
unzip -o LNL_libsubway_* -d ${CAMERA_SW}/Camera/Platform/LNL/MFTPlugin/libsubway/x64/LNL
cd ..

#  missing header 
mkdir -p ${CAMERA_SW}/Camera/xos/ia-imaging-control/ia_log/ia_log
cp -pv ia_time_meas.h ${CAMERA_SW}/Camera/xos/ia-imaging-control/ia_log/ia_log

# missing binary 
#cp -rv c:/Users/mandyhsi/OneDrive\ -\ Intel\ Corporation/Documents/ICE_docs/Tools/Composer\ XE\ 2013/*  ${CAMERA_SW}/Camera/MFTPlugin/Composer\ XE\ 2013
}

POSITIONAL_ARGS=()

if [ $# -eq 0 ]
  then
    echo "No arguments supplied. "
	echo "usage :   "
	echo "           ./${0##*/} -p [prebuild_path] -s [source_path]"
	echo "example : "
	echo "           ./${0##*/} -p ./prebuild_8313 -s ./vieddrv-github/w/camerasw/Source"
	exit -1
fi

while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--prebuild_dir)
      PREBUILD_DIR="$2"
      shift # past argument
      shift # past value
      ;;
    -s|--source_dir)
      SRC_DIR="$2"
      shift # past argument
      shift # past value
      ;;
	-d|--default)
      DEFAULT=YES
      shift # past argument with no value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

echo "PREBUILD  = ${PREBUILD_DIR}"
echo "SRC_DIR   = ${SRC_DIR}"
echo "DEFAULT   = ${DEFAULT}"
echo "ROOT = ${DEFAULT_ROOT}"
#echo "Number files in SEARCH PATH with EXTENSION:" $(ls -1 "${SEARCHPATH}"/*."${EXTENSION}" | wc -l)


if [ -d "${PREBUILD_DIR}" ]; then
  ### Take action if $DIR exists ###
  echo "extract files from ${PREBUILD_DIR}..."
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo "Error: ${PREBUILD_DIR} not found. Can not continue."
  exit 1
fi

extract

#if [[ -n $1 ]]; then
#   echo "Last line of file specified as non-opt/last argument:"
#fi

