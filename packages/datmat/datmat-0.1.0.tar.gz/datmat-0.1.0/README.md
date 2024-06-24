# Data Materialisation


## Getting started

Install `datmat` from PyPI:
```commandline
pip install datmat
```

In `datmat` you can interface with multiple data sources and storage solutions through a plugin system.
By linking together different plugins you can move data from one place to another.
A set of plugins is already installed when installing the package, but the program is set up to support development
of custom plugins. The plugins can be called by using a URL scheme to preface the path or URL to your file. For example,
by using `file:///home/user/file.txt` you can access the local file `/home/user/file.txt`, or by using
`xnat+https://xnat.bmia.nl/projects/sandbox` you can access the XNAT project `sandbox` on `xnat.bmia.nl` over HTTPS.

See below examples of various use cases.

## Downloading from XNAT into EUCAIM directory structure

Through the use of the `xnat+https://` plugin it is possible to download files from an XNAT instance.
The `eucaimdir://` plugin will store the files in the destination folder in the following nested folder structure:

```
/dest_folder/project_name/subject_label/experiment_label/{scan_id}_{scan_type}/file
```

The path `/dest_folder` needs to be supplied with the starting `/`, so the URL will be `eucaimdir:///dest_folder`.

### A complete project

```python
import datmat

datmat.materialize('xnat+https://xnat.bmia.nl/projects/sandbox',
                   'eucaimdir:///dest_folder',
                   tempdir='/temp_directory')
```

### A single subject
```python
import datmat

datmat.materialize('xnat+https://xnat.bmia.nl/search?projects=sandbox&subjects=TEST01&resources=DICOM',
                   'eucaimdir:///dest_folder',
                   tempdir='/temp_directory')
```

The `datmat` package is based on the IOPlugin system of Fastr. See the documentation for the [XNATStorage IOPlugin](https://fastr.readthedocs.io/en/stable/_autogen/fastr.reference.html#xnatstorage)
for more information on querying XNAT.

# Other use cases
## Copy file to file
```python
import datmat

datmat.materialize('file:///input_file',
                   'file:///dest_file',
                   tempdir='/temp_directory')
```

## Copy XNAT to XNAT
To be implemented.
