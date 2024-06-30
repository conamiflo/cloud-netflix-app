import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {map, Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  constructor(private httpClient: HttpClient) {}

}
