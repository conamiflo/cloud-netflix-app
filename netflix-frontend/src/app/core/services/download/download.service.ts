import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class FileDownloadService {

  constructor(private http: HttpClient) { }

  downloadFileFromPresignedUrl(url: string) {
    return this.http.get(url, { responseType: 'blob' });
  }
}
