#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
#from httplib2 import Http
from google.oauth2 import service_account
#from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload
from datetime import datetime

# Local source
import configs
from filemanager import printlog

sys.excepthook = sys.__excepthook__

class GoogleService:

    def __init__(self):

        self.spreadsheet_id = configs.SPREADSHEET_ID
        self.sheets = {
                    'ix': configs.IX_SHEET,
                    'progrun': configs.STARTS_SHEET,
                    'ping': configs.PING_SHEET,
                    'system': configs.SYSTEM_SHEET
                }

        self.nof_rows_left = 100
        self.quota_timer = datetime.now() # The service account has request quota of 100 requests per 100 seconds

        SERVICE_ACCOUNT_FILE = configs.service_account_file
        SCOPE = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

        self.creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)

        # Service for Google Sheets
        try:
            printlog('Gservice','Logging into Google Sheets..')
            self.gsheets = build('sheets', 'v4', credentials=self.creds)
            printlog('Gservice','Logging into Google Drive..')
            self.gdrive = build('drive', 'v3', credentials=self.creds)
        except Exception as e:
            printlog('Gservice','Could not log into google services: {}'.format(type(e).__name__, e))
        # self.creds.expiry = None so the credentials should not expire ever


# Sheets

    def _reduce_nof_rows_left(self, amount):
        # TODO are the quotas still same?
        pass
        self.nof_rows_left = (self.nof_rows_left - amount)
        if (self.nof_rows_left < 10):
            printlog('Gservice','Less than 10 ({}) rows left in quota'.format(self.nof_rows_left))
        return self.nof_rows_left


    def check_quota_timer(self):
        # reset log timer every 100s – quota for google is 100 requests per 100 seconds
        pass
        diff = (datetime.now()-self.quota_timer).total_seconds()
        if diff >= 100:
            self.quota_timer = datetime.now()
            self.nof_rows_left = 100
            timeLeft = 0


    def log_to_drive(self, data, sheet):

        rowLimit = self.nof_rows_left
        if rowLimit == 0:
            # Quota is full ATM
            return data

        dataToLog = data
        truncated = False

        if len(data) > rowLimit:
            dataToLog = data[0:rowLimit]
            truncated = True

        spreadsheet_id = self.spreadsheet_id
        value_input_option = 'USER_ENTERED'

        body = {
            'values': dataToLog
        }

        try:
            range_name = self.sheets[sheet]
        except:
            printlog('Gservice','ERROR: No such sheet.')

        try:

            result = self.gsheets.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id, range=range_name,
                valueInputOption=value_input_option, body=body).execute()

            printlog('Gservice','{0} cells appended.'.format(result \
                                                   .get('updates') \
                                                   .get('updatedCells')))
        except:
            printlog('Gservice', 'ERROR: Uplaoding to sheets failed.')

        self._reduce_nof_rows_left(len(dataToLog))
        dataLeft = []

        if truncated:
            dataLeft = data[rowLimit:]

        return dataLeft

# Drive

    def _upload_file(self, localFilePath, metadata):
        # general module to upload any file to specified folder in Google Drive

        printlog('Drive','Uplaoding file: {}'.format(localFilePath))

        media = MediaFileUpload(
            localFilePath,
            mimetype=metadata['mimeType']
            )
        try:
            file = self.gdrive.files().create(
                body=metadata,
                media_body=media,
                fields='id'
                ).execute()
        except Exception as e:
            printlog('Drive','ERROR: could not upload file. Emessage: {}'.format(e))
            raise e

        fileId = file.get('id')
        printlog('Drive','Uploaded file {} of type {} with id {}.'.format(
                metadata['name'], metadata['mimeType'], fileId))
        return fileId


    def create_folder(self, folderName, parentFolder=None):

        if not parentFolder:
            metadata = {
                'name': folderName,
                'mimeType': 'application/vnd.google-apps.folder',
                }
        else:
            metadata = {
                'name': folderName,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parentFolder]
                }
        try:
            folder = self.gdrive.files().create(
                    body=metadata,
                    fields='id'
                ).execute()
        except Exception as e:
            printlog('Drive','ERROR: could not create folder. Emessage: {}'.format(e))
            raise e

        folderId = folder.get('id')
        printlog('Drive','Created folder {} with id {}.'.format(
                    metadata['name'], folderId))
        return folderId


    def list_content(self):

        results = self.gdrive.files().list(
                pageSize=1000, fields="nextPageToken, files(id, name, mimeType)").execute()
        files = {}
        folders = {}
        for item in results['files']:
            if item['mimeType'] != 'application/vnd.google-apps.folder':
                files[item['name']] = item['id']
            else:
                folders[item['name']] = item['id']

        return files, folders


    def upload_recording(self, fileName, parentFolderId, directory):
        # Upload video file from the local camera-records folder
        localFilePath = directory + fileName
        metadata = {
            'name': fileName,
            'mimeType': '*/*',
            'parents':[parentFolderId]
            }

        fileId = self._upload_file(localFilePath, metadata)


    def upload_logfile(self, fileName):
        # Upload local logfile to drive from dir sakis-video-tunnel
        localFilePath = configs.root + fileName
        metadata = {
            'name': datetime.now().strftime("%m-%d_%H-%M") + '_' + fileName,
            'mimeType': '*/*',
            'parents': [configs.GDRIVE_FOLDER_ID_LOGS]
            }

        fileId = self._upload_file(localFilePath, metadata)


    def delete_resource(self, resourceId):

        try:
            self.gdrive.files().delete(fileId=resourceId).execute()
            printlog('Gservice','Deleted resource with id {}'.format(resourceId))
        except Exception as e:
            printlog('Gservice','ERROR: Could not delete file. Emessage:', e)


    def delete_videos(self):

        content = self.list_content()
        videoIds = []
        for file in content:
            if file.endswith('.h264'):
                id = content[file]
                videoIds.append(id)

        for vid in videoIds:
            self.delete_resource(vid)
