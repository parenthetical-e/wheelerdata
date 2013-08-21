# Add new dirs
mkdir fidl
mkdir archive
mkdir mvpa

# Archive old data
mv analysis/ archive/
mv atlas/ archive/
mv QA/ archive/
mv loc/ archive/
mv run* archive/

# Move the fidls
mv *.fidl fidl/

# And archive the rst
mv *.* ./archive/

# Restructure the .dcm files
cd raw/
sh ~/src/metaaccumulate/mniconvert/studyrename.sh
mv study* ../
cd ../
rmdir raw/