# MoEDAL NTD Scan Processing

_Note: this is work in progress and subject to change._

##Getting the code

```bash
$ cd $WORKING_DIR # Your working directory.
$ git clone https://github.com/twhyntie/moedal-ntd-data-profiles.git
$ cd moedal-ntd-data-profiles
```

_TODO: Get the Python library dependencies needed to run the scripts_.


##Converting the BMP files

In order to process the files with `matplotlib`, the original scan images need to be converted into the PNG format.

```bash
$ mkdir ../montage
$ python convert-scans.py testdata/ ../montage/.
[...]
* Converting '00000.bmp' -> '../tmp3/00000.png'.
```


##Splitting the PNG file

The original scan images (to date) are presented as a montage of smaller images. We actually need the individual smaller images, so we'll use this script to split them up.

```bash
$ mkdir ../split
$ python split-scans.py ../montage/00000.png ../split/.
```

This should produce 108 scan images in the `../split` output directory.


##Scaling the scans
The individual scan images (to date) are a bit too small for Panoptes, so we use a few handy Python libraries to scale them up by a factor of 5.

```bash
$ mkdir ../scaled
$ python scale-scans.py ../split/ ../scaled/.
```


##Creating the Panoptes manifest
Pantoptes Subject Sets require a Comma Separated Value **manifest** file to supply the subject **metadata** when uploading to Panoptes. The following script creates this in the output directory so that the subject set is ready for upload.

```bash
$ python create-manifest.py ../scaled/ ../scaled/
```

The manifest in this case should look like this:
```
$ cat ../scaled/manifest.csv
id,row_id,col_id,magnification,filename
00000_00_00,0,0,5,00000_00_00.png
[...]
00000_08_11,8,11,5,00000_08_11.png
```

You should now be able to upload the contents of the `../scaled` directory (108 images, 1 manifest) to your Panoptes project via the Subject Set interface.


##Useful links

* [Panoptes](http://preview.zooniverse.org/panoptes/#).
