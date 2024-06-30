import {Component, Input} from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import {MovieService} from "../../../../../core/services/movie/movie.service";

@Component({
  selector: 'app-movie-card',
  standalone: true,
  imports: [MatCardModule],
  templateUrl: './movie-card.component.html',
  styleUrl: './movie-card.component.css'
})

export class MovieCardComponent {
  // @Input() movie: any;
  //
  // constructor(private movieService: MovieService) {}
  //
  // ngOnInit() {
  //   this.movieService.getMovieByIdAndTitle(this.movie.movie_id, this.movie.title).subscribe(
  //     (data) => {
  //       this.movie = data;
  //     },
  //     (error) => {
  //       console.error('Error fetching movie data', error);
  //     }
  //   );
  // }
}
