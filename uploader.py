import sys
import filemanager

print('subprocess')

records, directory = filemanager.list_recordings()
print(sys.argv[0])
not_permitted = sys.argv[1]
folderId = sys.argv[2]

SERVICE_ACCOUNT_FILE = '/home/pi/sakis-tunnel-2021/service_account.json'
SCOPE = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

CREDS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)

gservice = build('drive', 'v3', credentials=CREDS)

filepath = "/home/pi/sakis-tunnel-2021/uploadlog.txt"
txt_file = open(filepath,'a+')
uploads = txt_file.readlines()

i = 0
for filename in records:
    if filename != not_permitted or filename in uploads:
        # skip if currently being recorded or was already tried before
        try:
            txt_file.write(filename)
            gservice.upload_recording(filename, folderId, directory)
            filemanager.delete_local_file(directory + filename)
            i += 1

        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filemanager.log_local(timestamp + ' Could not upload file: {}, error: {}'.format(filename, type(e).__name__, e),'uploader.csv')

            if type(e).__name__ == "TimeoutError":
                break

txt_file.close()
