# edge_assessment

[![standard-readme compliant](https://img.shields.io/badge/edge%20assessment-standard-brightgreen.svg?style=flat-square)](https://github.com/Remote-Sensing-of-Land-Resource-Lab/AssessEdge)

An assessment tool for evaluating the quality of object edges within an input map.

![](/images/pic1.jpg "Agricultural Field Delineation")

## Table of Contents
  * [Background](#background)
  * [Install](#install)
  * [Usage](#usage)
  * [Contributors](#contributors)
  * [License](#license)

## Background

An accurate delineation of edge is critical for object-based image analysis on land resources such as agricultural field objects and building objects, and change detection particularly for climate-induced land change such as snow melting and treeline shifts.  The traditional F1-score has been widely used for assessing map quality, which, however, often fails to provide information on object boundary quality. To address this problem, we developed a new evaluation index to take account of both thematic and edge accuracy.

## Install
Install AssessEdge using `pip`:

```bash
pip install AssessEdge
```

Use requirements.txt to install the required packages.

```bash
pip install -r requirements.txt
```

## Usage

The two main functions are `eval_edge` and `plot_results` in `edge_buffer.py`

`eval_edge(testing_field, reference_field, step, min_width, initial_max_width)`: input two variables(testing_field & reference_field), the testing_field represents the result of classification, the reference_field represents the real reference object field. The pixel values of target objects should be processed as 1, and pixel values of background should be 0 or no data. The function will return a dictionary include commission error, omission error, edge f1 score, middle point, etc. The `step` defaults as 3, the `initial_max_width` defaults as 0, and the `min_width` defaults as 3.

`plot_results`: show the testing_field and reference_field data fit curves and their data points. 

Users can type the following codes to use these two functions

```bash
from AssessEdge import eval_edge, plot_results
from AssessEdge import rasterio_loaddata

def main(map_path, reference_path):
    map_path = "/images/testing_field.tif"
    reference_path = "/images/reference_field.tif"
    map_array = rasterio_loaddata(map_path)
    reference_array = rasterio_loaddata(reference_path)
    result = eval_edge(map_array, reference_array)
    plot_results(result)

if __name__ == "__main__":
    main()
```

### Test 
Testing images have been placed in the images folder.
The test procedure is assess_image.py in test folder. To test it 
```bash
python assess_image.py --map_path map_path --reference_path reference_path
```
It will show the test result as following
![](/images/test_result.png "Test result")

## Contributors

Yingfan Zhang (zhangyingfanuk@163.com), Su Ye

## License

[Apache License](LICENSE)