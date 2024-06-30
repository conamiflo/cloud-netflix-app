import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {environment} from "../../../../env/env";

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  constructor(private httpClient: HttpClient) {}

  getAllMovies(): Observable<any> {
    return this.httpClient.get(environment.cloudHost + 'movies');
  }

  getMovieById(movieId: string): Observable<any> {
    return this.httpClient.get(environment.cloudHost + 'movies/${movieId}');
  }

  getMovieByIdAndTitle(movieId: string, title: string): Observable<any> {
    let params = new HttpParams()
      .set('title', title)
      .set('movie_id', movieId);

    return this.httpClient.get(environment.cloudHost + 'movies', { params });
  }

}
