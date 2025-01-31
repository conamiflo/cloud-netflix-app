import { Component } from '@angular/core';
import {MovieCardComponent} from "../movies/movie-card/movie-card.component";
import {MovieService} from "../../../../core/services/movie/movie.service";
import {CommonModule, NgFor} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {CognitoService} from "../../../../core/services/cognito/cognito.service";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [MovieCardComponent, NgFor, CommonModule, FormsModule],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {
  movies: any[] = [];
  title: string = '';
  description: string = '';
  actors: string = '';
  directors: string = '';
  genres: string = '';

  constructor(private movieService: MovieService,
              private cognitoService: CognitoService,
  ) {}

  ngOnInit() {
    this.cognitoService.getUsername().then(async username => {
      if (username) {
        (await this.movieService.getFeed(username)).subscribe(
          (data) => {
            this.movies = data.movies;
            console.log(data);
          },
          (error) => {
            console.error('Error fetching movies', error);
          }
        );
      } else {
        console.error('No username found. User may not be logged in.');
      }
    });
  }

  async searchMovies() {
    const actors = this.actors.split(',').map(actor => actor.trim());
    const directors = this.directors.split(',').map(director => director.trim());
    const genres = this.genres.split(',').map(genre => genre.trim());

    (await this.movieService.searchMovies(this.title, this.description, actors, directors, genres)).subscribe(
      (data) => {
        this.movies = data;
      },
      (error) => {
        console.error('Error searching movies', error);
      }
    );
  }

}
