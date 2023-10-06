from django.shortcuts import render
from .ftpsettings import FTP_SERVER,FTP_PASSWORD,FTP_USERNAME
# Create your views here.
from django.shortcuts import render

from django.http import StreamingHttpResponse, HttpResponse,JsonResponse
from wsgiref.util import FileWrapper
from detailapp.models import Order_Product
import ftputil
import os

def download_list(request):
    try:
        user=request.user
        order_items=Order_Product.objects.filter(user=user)
        
        # Connect to the FTP server

        # Define source path (FTP server's home folder) and destination path (user's local download folder)

        return render(request, 'download-list.html', {'orders': order_items})
    except Exception as e:
        # Handle FTP connection errors gracefully
        return e

def inc_counter(request,id):
    order=Order_Product.objects.get(id=id)
    order.counter=order.counter+1
    order.save()
    return JsonResponse({'status':True,'counter':order.counter})


def file_download(request,filename):
    try:
        host = ftputil.FTPHost(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)
        # Define source path (FTP server's home folder) and destination path (user's local download folder)
        source_folder = "."  # Replace with the actual path on the FTP server

        # Change to the source path on the FTP server
        host.chdir(source_folder)
        source_path = os.path.join(source_folder, filename)  # define the extension yourself mainly mp4

        remote_file = host.open(source_path, 'rb')
        remote_file_size = host.path.getsize(source_path)

        chunk_size = 36192 # You can adjust this value as needed

            # Create a response with a custom file wrapper that limits download speed
        
        response = StreamingHttpResponse((chunk for chunk in iter(lambda: remote_file.read(chunk_size), b'')), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = remote_file_size  # Set the total file size

        # Set Accept-Ranges header to enable partial content requests
        response['Accept-Ranges'] = 'bytes'

            # Limit the download speed to 1 MB/s (adjust as needed)
        # response['X-Accel-Buffering'] = 'no'
        # response['X-Accel-Limit-Rate'] = '1024k'
        return response

       
    except Exception as e:
        # Handle FTP connection errors gracefully
        return render(request,'404.html')
