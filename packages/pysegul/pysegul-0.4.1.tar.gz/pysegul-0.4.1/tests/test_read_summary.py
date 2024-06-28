import pysegul

from os import listdir

def test_read_summary(tmp_path):
    input_dir = 'tests/raw-data'
    input_format = 'auto'
    summary_mode = 'default'
    prefix = 'read_summary'
    output_path = tmp_path.joinpath('results')
    output_dir = str(output_path)
    summary = pysegul.ReadSummary(
        input_format,  
        summary_mode,
        output_dir,
        prefix
        )
    summary.from_dir(input_dir)
    assert output_path.exists()
    # Check if the output directory contains the expected files
    results = listdir(output_path)
    assert len(results) == 1