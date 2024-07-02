import { Component } from '@angular/core';
import {MovieCardComponent} from "../movies/movie-card/movie-card.component";
import {MovieService} from "../../../../core/services/movie/movie.service";
import {CommonModule, NgFor} from "@angular/common";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [MovieCardComponent,NgFor,CommonModule],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {
  movies: any[] = [];

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

}
