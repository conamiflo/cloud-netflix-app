import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {environment} from "../../../../env/env";

@Injectable({
  providedIn: 'root'
})
export class ReviewService {
  constructor(private httpClient: HttpClient) {}

  submitReview(username: string, movie_id: string, value: number): Observable<any> {
    const url = environment.cloudHost + 'reviews'; // Update with your actual endpoint
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = {
      username,
      movie_id,
      value
    };

    return this.httpClient.post(url, JSON.stringify(body), { headers });
  }

}
