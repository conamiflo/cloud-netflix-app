import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {environment} from "../../../../env/env";
import {CognitoService} from "../cognito/cognito.service";

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  constructor(private httpClient: HttpClient,private cognitoService:CognitoService) {}
  headers = new Headers();

  async getAllMovies(): Promise<Observable<any>> {

    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationToken', value as string);
    headers.append('authorizationToken', value);
    return this.httpClient.get(environment.cloudHost + 'movies',{ headers });
  }

  async getMovieById(movieId: string): Promise<Observable<any>> {
    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationToken', value as string);
    headers.append('authorizationToken', value);
    return this.httpClient.get(environment.cloudHost + 'movies/${movieId}',{headers});
  }

  async getMovieByIdAndTitle(movieId: string, title: string): Promise<Observable<any>> {
    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationToken', value as string);
    headers.append('authorizationToken', value);

    let params = new HttpParams()
      .set('title', title)
      .set('movie_id', movieId);

    return this.httpClient.get(environment.cloudHost + 'movies', {headers,params});
  }

  async getFeed(username: string): Promise<Observable<any>> {
    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationToken', value as string);
    headers.append('authorizationToken', value);

    let params = new HttpParams()
      .set('username', username);

    return this.httpClient.get(environment.cloudHost + 'feed', {headers, params});
  }

  async searchMovies(title: string, description: string, actors: string[], directors: string[], genres: string[]): Promise<Observable<any>> {

    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationToken', value as string);
    headers.append('authorizationToken', value);

    const url = environment.cloudHost + 'search';

    let params = new HttpParams()
      .set('title', title)
      .set('description', description);
    if (actors.length > 0) {
      params = params.set('actors', actors.join(','));
    }
    if (directors.length > 0) {
      params = params.set('directors', directors.join(','));
    }
    if (genres.length > 0) {
      params = params.set('genres', genres.join(','));
    }

    return this.httpClient.get(url, {headers,params});
  }

  async createMovie(movieData: any): Promise<Observable<any>> {

    var value = await this.cognitoService.getJWT()


    const url = environment.cloudHost + 'movies';
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    headers.append('authorizationToken', value);
    return this.httpClient.post(url, JSON.stringify(movieData), {headers});
  }

  async downloadMovie(username: string, movieId: string): Promise<Observable<any>> {

    var value = await this.cognitoService.getJWT()

    const url = environment.cloudHost + 'history';
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    headers.append('authorizationToken', value)

    const body = {username, movie_id: movieId};
    return this.httpClient.post(url, JSON.stringify(body), {headers});
  }

  async deleteMovie(movieId: string, title: string): Promise<Observable<any>> {

    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationToken', value as string);
    headers.append('authorizationToken', value);

    const url = environment.cloudHost + 'movies';
    const params = new HttpParams()
      .set('movie_id', movieId)
      .set('title', title);
    return this.httpClient.delete(url, {headers, params});

  }

  async getMoviesBySeries(series: string, excludeMovieId: string): Promise<Observable<any>> {

    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationToken', value as string);
    headers.append('authorizationToken', value);

    const url = environment.cloudHost + 'series';
    let params = new HttpParams()
      .set('series', series)
      .set('exclude_movie_id', excludeMovieId);

    return this.httpClient.get(url, {headers,params});
  }

  async editMovie(movieId: string, movieData: any): Promise<Observable<any>> {

    var value = await this.cognitoService.getJWT()


    const url = environment.cloudHost + 'movies';
    const body = {
      movie_id: movieId,
      ...movieData
    };
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    headers.append('authorizationToken', value);
    return this.httpClient.put(url, JSON.stringify(body), {headers});
  }

}
