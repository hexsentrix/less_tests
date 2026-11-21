source venv/bin/activate
cd tests_data && time python ../src/test.py && python ../eval_local.py output.json answers.json && cd ..
