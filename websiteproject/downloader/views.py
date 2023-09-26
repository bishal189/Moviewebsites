from django.shortcuts import render
from .ftpsettings import FTP_SERVER,FTP_PASSWORD,FTP_USERNAME
# Create your views here.
from django.shortcuts import render

from django.http import FileResponse,HttpResponse,JsonResponse
from wsgiref.util import FileWrapper
from detailapp.models import Order_Product
import ftputil
import os

def download_list(request):
    try:
        user=request.user
        order_items=Order_Product.objects.filter(user=user)
        
        # Connect to the FTP server
        host = ftputil.FTPHost(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)

        # Define source path (FTP server's home folder) and destination path (user's local download folder)
        source_path = "."  # Replace with the actual path on the FTP server

        # Change to the source path on the FTP server
        host.chdir(source_path)

        # Get a list of files in the source path

        # Close the FTP connection
        host.close()
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
        source_path = os.path.join(source_folder, filename+".iso")  # define the extension yourself mainly mp4


        # Check if the file exists on the FTP server
        # if not host.download_if_newer(source_path, filename):
        #     return render(request, '404.html')
            # Serve the downloaded file
        remote_file = host.open(source_path, 'rb')

            # Create a response with a custom file wrapper that limits download speed
        response = HttpResponse(FileWrapper(remote_file), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Limit the download speed to 1 MB/s (adjust as needed)
        response['X-Accel-Buffering'] = 'no'
        response['X-Accel-Limit-Rate'] = '1024k'
        return response

       
    except Exception as e:
        # Handle FTP connection errors gracefully
        return render(request, '404.html')
