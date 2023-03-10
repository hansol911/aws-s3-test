import boto3
import json
import base64
import re
import magic
import duplicate

def validate_file(file, presignedURL):
    if file == None:
        return 'File should be attached.'
        
    # file extension check
    regex_file_whitelist = "^.*(7z|ai|alz|apk|avi|bmp|csv|doc|docm|docx|egg|eps|fla|flv|gif|hwp|hwt|jpeg|jpg|m4v|mht|mov|mp3|mp4|pdf|png|potx|pps|ppsm|ppsx|ppt|pptm|pptx|psd|rar|rtf|show|svg|swf|tif|tiff|ttf|txt|wav|webm|webp|wmv|xls|xlsb|xlsm|xlsx|zip)$"
    type = (file['type'].decode('utf-8')).split("/")[1]
    
    if re.match(regex_file_whitelist, type) == None:
        return 'Not a valid file extension.'
    
    # magic - file validation check
    mime_type_whitelist = ["x-softmaker-pm",
      "application/x-7z-compressed",
      "application/pdf",
      "application/x-alz",
      "application/vnd.android.package-archive",
      "application/msword",
      "application/vnd.adobe.fla",
      "application/x-hwp",
      "application/haansofthwp",
      "application/vnd.hancom.hwp",
      "application/x-hwt",
      "application/haansofthwt",
      "application/vnd.hancom.hwt",
      "application/pdf",
      "application/vnd.ms-powerpoint",
      "application/vnd.ms-powerpoint.slideshow.macroEnabled.12",
      "application/vnd.ms-powerpoint",
      "application/vnd.ms-powerpoint.presentation.macroEnabled.12",
      "application/rtf",
      "application/haansoftjustslideshow",
      "application/haansoftshow",
      "application/ttf",
      "application/haansoftxls",
      "application/kset",
      "application/msexcell",
      "application/softgrid-xls",
      "application/vnd.ms-excel",
      "application/x-rar",
      "application/x-rar-compressed",
      "application/x-shockwave-flash",
      "application/zip",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/vnd.ms-word.document.macroEnabled.12",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/vnd.ms-excel.sheet.macroEnabled.12",
      "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
      "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      "application/vnd.openxmlformats-officedocument.presentationml.template",
      "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
      "application/illustrator",
      "application/hwp",
      "text/plain",
      "text/x-comma-separated-values",
      "image/webp",
      "image/bmp",
      "image/gif",
      "image/jpeg",
      "image/png",
      "image/svg+xml",
      "image/tiff",
      "image/x-eps",
      "image/x-psd",
      "audio/mpeg",
      "audio/x-wav",
      "video/x-flv",
      "video/x-m4v",
      "video/mp4",
      "video/vp8",
      "video/webm",
      "video/x-webm",
      "video/quicktime",
      "video/x-ms-wmv",
      "video/x-msvideo"]
        
    mime_type = magic.from_buffer(file['content'][:2048], mime=True)
    
    if mime_type not in mime_type_whitelist:
        return {'statusCode': 400, 'message': 'Not a valid mime type'}
       
    # file 용량 제한 (100MB) ## todo : 서버에 검증요청
    file_size = len(file['content'])
    limit_size = 100 * 1024 * 1024
    
    if file_size > limit_size:
        return {'statusCode': 400, 'message': 'File size too large'}
    
    # file name check (중복된 이름이 있는지 확인)
    url = presignedURL['content'].decode('utf-8')
    filename = duplicate.check_filename(url, file)
    
    return {'statusCode': 200, 'message': {'type': mime_type, 'size': file_size, 'filename': filename}}
    