from django.shortcuts import render
from .ftpsettings import FTP_SERVER,FTP_PASSWORD,FTP_USERNAME
from django.shortcuts import render
from django.http import StreamingHttpResponse,JsonResponse
from detailapp.models import Order_Product,Order_Product_album
from albums.models import AlbumMovie
import ftputil
import os
from .createuser import CreateUser
import os
import subprocess

#List all the downloads in download page 
def download_list(request):
    
        user=request.user
        CreateUser(user.username)
        order_items=Order_Product.objects.filter(user=user)
        user_home_directory = "/home/"+user.username        
        centralized_movies_directory = "/home/website"

        for item in order_items:
            purchased_movie = item.product.movie_name

# Create a symbolic link to the purchased movie
            symlink_path = os.path.join(user_home_directory, purchased_movie)
            source_path = os.path.join(centralized_movies_directory,purchased_movie)
            command = ["sudo", "ln", "-s", source_path, symlink_path]
            try:
                subprocess.run(command, check=True)
                print("Symbolic link created successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
            
            albums=Order_Product_album.objects.filter(user=user)
        for album in albums:
            albumdir=os.path.join(user_home_directory,album.product.album.album_name)
            subprocess.run(['sudo','mkdir','-p',albumdir],check=True)

            for movie in album.product.movies.all():
                purchased_movie=movie.movie_name
                symlink_path = os.path.join(albumdir, purchased_movie)
                source_path = os.path.join(centralized_movies_directory,purchased_movie)
                command = ["sudo", "ln", "-s", source_path, symlink_path]
                try:
                    subprocess.run(command, check=True)
                    print("Symbolic link created successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")

        return render(request, 'download-list.html', {'orders': order_items,'albums':albums})
    

def package_list(request,id):
    album=AlbumMovie.objects.get(id=id)
    movies=album.movies.all()
    return render(request,'package-list.html',{'orders':movies})
    
#increases the counter since one movie can only be downloaded 3 times 
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

        chunk_size = 36192 # You can adjust this value as needed default was 8192

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
