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

  getFeed(username: string): Observable<any> {
    let params = new HttpParams()
      .set('username', username);

    return this.httpClient.get(environment.cloudHost + 'feed', { params });
  }

  searchMovies(title: string, description: string, actors: string, directors: string, genres: string): Observable<any> {
    let params = new HttpParams()
      .set('title', title)
      .set('description', description)
      .set('actors', actors)
      .set('directors', directors)
      .set('genres', genres);

    return this.httpClient.get(environment.cloudHost + 'search', { params });
  }

}
