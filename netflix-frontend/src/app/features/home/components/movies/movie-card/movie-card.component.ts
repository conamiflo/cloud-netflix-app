import {Component, Input} from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import {MovieService} from "../../../../../core/services/movie/movie.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-movie-card',
  standalone: true,
  imports: [MatCardModule],
  templateUrl: './movie-card.component.html',
  styleUrl: './movie-card.component.css'
})

export class MovieCardComponent {
  @Input() movie: any;

  constructor(private router: Router) {}

  navigateToMovieDetails() {
    this.router.navigate(['/movies', this.movie.movie_id, this.movie.title]);
  }
}
