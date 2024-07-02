import { Component } from '@angular/core';
import {MovieCardComponent} from "../movies/movie-card/movie-card.component";
import {MovieService} from "../../../../core/services/movie/movie.service";
import {CommonModule, NgFor} from "@angular/common";
import {FormsModule} from "@angular/forms";

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

  constructor(private movieService: MovieService) {}

  ngOnInit() {
    this.movieService.getFeed('Borizzlav-Celar').subscribe(
      (data) => {
        this.movies = data.movies;
      },
      (error) => {
        console.error('Error fetching movies', error);
      }
    );
  }

  searchMovies() {
    console.log(this.title,this.description,this.actors,this.directors,this.genres)
    this.movieService.searchMovies(this.title, this.description, this.actors, this.directors, this.genres).subscribe(
      (data) => {
        this.movies = data;
      },
      (error) => {
        console.error('Error searching movies', error);
      }
    );
  }

}
