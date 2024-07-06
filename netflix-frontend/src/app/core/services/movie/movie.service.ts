import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
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

  createMovie(movieData: any): Observable<any> {
    const url = environment.cloudHost + 'movies';
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.httpClient.post(url, JSON.stringify(movieData), { headers });
  }

  downloadMovie(username: string, movieId: string): Observable<any> {
    const url = environment.cloudHost + 'history';
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = { username, movie_id: movieId };
    return this.httpClient.post(url, JSON.stringify(body), { headers });
  }

  deleteMovie(movieId: string, title: string): Observable<any> {
    const url = environment.cloudHost + 'movies';
    const params = new HttpParams()
      .set('movie_id', movieId)
      .set('title', title);
    return this.httpClient.delete(url, { params });

  }

  getMoviesBySeries(series: string, excludeMovieId: string): Observable<any> {
    const url = environment.cloudHost + 'series';
    let params = new HttpParams()
      .set('series', series)
      .set('exclude_movie_id', excludeMovieId);

    return this.httpClient.get(url, { params });
  }

  editMovie(movieId: string, movieData: any): Observable<any> {
    const url = environment.cloudHost + 'movies';
    const body = {
      movie_id: movieId,
      ...movieData
    };
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.httpClient.put(url, JSON.stringify(body), { headers });
  }

}
