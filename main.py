import io
from fastapi import FastAPI,File,UploadFile,HTTPException
from b2sdk.v2 import InMemoryAccountInfo,B2Api
import shutil 
import os
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = {
    "http://127.0.0.1.tiangolo.com",
    "https://127.0.0.1.tiangolo.com",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

info = InMemoryAccountInfo()
b2_api = B2Api(info)
app_key = "K005RVRokrCOJcQ9tSDLq8aDHajziKM"
app_key_ID = "005daaffbb3b1180000000002"
bucket_name = "mc-upload-bk"
b2_api.authorize_account('production',application_key=app_key,application_key_id=app_key_ID) #'Your-Application-Key-ID','Your-Application-key'



@app.get('/get_upload_url/')
async def get_upload_url(file_name:str,):
    bucket = b2_api.get_bucket_by_name(bucket_name=bucket_name) #Bucket-Name
    upload_response_url= bucket.upload_local_file(
    file_name=file_name,
    )
    return {
        "uploadUrl": upload_response_url["url"],
        "authorizationToken": upload_response_url["authorizationToken"]
    }

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:

        file_Content = await file.read()
        file_stream = io.BytesIO(file_Content)

        # with open(file_path, "wb") as buffer:
        #     shutil.copyfileobj(file.file,buffer)
        print(f"File to be : {file.filename}")
        
        # if not os.path.exists(file.filename):
        #     raise HTTPException(status_code=500, detail="File Not Found !@")
        
        bucket = b2_api.get_bucket_by_name(bucket_name)
        bucket.upload_bytes(
            data_bytes=file_stream.getvalue(),
            file_name=file.filename
        )

        # upload_url_response = await get_upload_url(file_name=file.filename)
        # upload_url = upload_url_response["uploadUrl"]
        # authorization_token = upload_url_response['authorizationToken']
        # headers = {
        #     "Authorization":authorization_token,
        #     "Content-Type":"application/octet-stream"
        # }
        file_info_dict = {
            # "fileId":file_info.file_id,
            # "file_name":file_info["file_name"],
            # "contentLength": file_info.content_length,
            # "contentType": file_info.content_type,
            # "uploadTimestamp": file_info.upload_timestamp

        }

        return {"message": f"File {file.filename} uploaded successfully"}
    
        # with open(file.filename,"rb") as file_content:
        #     print(f"CONTENT:{file_content}")
        #     response = requests.put(upload_url,headers=headers,data=file_content)
        #     if response.status_code == 200:
        #         return {
        #             "message": f"File {file.filename} uploaded successfully"
        #         }
        #     else :
        #         return {"message": f"Failed to upload file: {response.text, response.status_code}"}

    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)} "}, status_code=500)



# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)