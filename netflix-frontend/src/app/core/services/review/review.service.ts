import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {environment} from "../../../../env/env";
import {CognitoService} from "../cognito/cognito.service";

@Injectable({
  providedIn: 'root'
})
export class ReviewService {
  constructor(private httpClient: HttpClient,private cognitoService:CognitoService) {}

  async submitReview(username: string, movie_id: string, value: number): Promise<Observable<any>> {
    var valueJwt = await this.cognitoService.getJWT()

    const url = environment.cloudHost + 'reviews'; // Update with your actual endpoint
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    headers.append('authorizationtoken', valueJwt as string)
    const body = {
      username,
      movie_id,
      value
    };

    return this.httpClient.post(url, JSON.stringify(body), {headers});
  }

  async getAllReviews(movieId: string): Promise<Observable<any>> {
    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationtoken', value as string);
    const url = environment.cloudHost + 'reviews';
    let params = new HttpParams()
      .set('movie_id', movieId);
    return this.httpClient.get(url, {headers,params});
  }

}
