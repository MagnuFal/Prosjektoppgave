from biapy import BiaPy

b = BiaPy(config="config_file.yaml",
          result_dir="result_dir",
          name="job_name",
          run_id=1,
          gpu="0")
b.test()