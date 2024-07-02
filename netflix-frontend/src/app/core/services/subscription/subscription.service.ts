import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {environment} from "../../../../env/env";

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  constructor(private httpClient: HttpClient) {}


}
