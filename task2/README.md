this is the step one of the final project "Chat Engine Assignment" where mutiple agents work togeter to perform rag operations.

we use/tech stack:
python 3.12
conda for venv
fastapi for api

how to use:
conda create final_project_alience_intern
conda activate final_project_alience_intern

sample test api:
bash```
curl.exe -X POST `
>>   -F "files=@storage/uploads/test_file-sample_150kB.pdf" `
>>   -F "files=@storage/uploads/test_sample.pdf" `
>>   http://127.0.0.1:8000/upload
```
