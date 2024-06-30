import { Component } from '@angular/core';
import {MovieCardComponent} from "../movies/movie-card/movie-card.component";
import {MovieService} from "../../../../core/services/movie/movie.service";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [MovieCardComponent],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {
  // movies: any[] = [];
  //
  // constructor(private movieService: MovieService) {}
  //
  // ngOnInit() {
  //   this.movieService.getAllMovies().subscribe(
  //     (data) => {
  //       this.movies = data;
  //     },
  //     (error) => {
  //       console.error('Error fetching movies', error);
  //     }
  //   );
  // }

}
