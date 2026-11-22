source venv/bin/activate
python -m unittest discover -s tests -v
cd tests_data && time python ../src/test.py && python ../eval_local.py output.json answers.json && cd ..
