import { Component, OnInit } from '@angular/core';
import { addIcons} from 'ionicons';
import {IonIcon} from '@ionic/angular/standalone'
import { cameraOutline, playCircle, shareSocial, play, downloadOutline, chevronUp ,calendarOutline,timeOutline,star,send} from 'ionicons/icons';
import {MovieReviewComponent} from "../movie-review/movie-review.component";
import {MovieCardComponent} from "../movie-card/movie-card.component";
import {MovieReviewDialogComponent} from "../movie-review-dialog/movie-review-dialog.component";
import {MatDialog} from "@angular/material/dialog";
import {MatFormField, MatLabel} from "@angular/material/form-field";
import {ActivatedRoute, Router} from "@angular/router";
import {MovieService} from "../../../../../core/services/movie/movie.service";
import {NgFor, NgIf} from "@angular/common";
import {CognitoService} from "../../../../../core/services/cognito/cognito.service";
import {ReviewService} from "../../../../../core/services/review/review.service";
import {ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-movie-details',
  standalone: true,
    imports: [IonIcon, MovieReviewComponent, MovieCardComponent, MatLabel, MatFormField, NgFor, ReactiveFormsModule,NgIf],
  templateUrl: './movie-details.component.html',
  styleUrl: './movie-details.component.css'
})
export class MovieDetailsComponent implements OnInit{
  constructor(public dialog: MatDialog,
              private route: ActivatedRoute,
              private movieService: MovieService,
              private cognitoService: CognitoService,
              private reviewService: ReviewService,
              private router:Router) {
    addIcons({ cameraOutline, playCircle, shareSocial, play, downloadOutline, chevronUp,calendarOutline,timeOutline,star,send});
  }
  movie: any;
  reviews: any[] = [];
  movies: any[] = [];

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const movieId = params.get('id');
      const movieTitle = params.get('title');
      if (movieId && movieTitle) {
        this.getMovie(movieId,movieTitle);
        this.getReviews(movieId);
      }
    });
  }

  editMovie() {
    this.router.navigate(['edit-movie', this.movie.movie_id, this.movie.title]);
  }

  getSeries(series: string, movieId : string){
    this.movieService.getMoviesBySeries(series,movieId).subscribe(
      (data) => {
        if (Array.isArray(data)) {
          this.movies = data;
        } else if (typeof data === 'object') {
          this.movies = [data];
        } else {
          this.movies = [];
        }
      },
      (error) => {
        console.error('Error fetching series', error);
      }
    );
  }

  getMovie(movieId: string, movieTitle : string){
    this.route.paramMap.subscribe(params => {
      const movieId = params.get('id');
      const movieTitle = params.get('title');

      if (movieId && movieTitle) {
        this.movieService.getMovieByIdAndTitle(movieId, movieTitle).subscribe(
          (data) => {
            this.movie = data;
            if (this.movie && this.movie.series) {
              this.getSeries(this.movie.series, movieId);
            }
          },
          (error) => {
            console.error('Error fetching movie data', error);
          }
        );
      }
    });
  }

  getReviews(movieId: string){
    this.reviewService.getAllReviews(movieId).subscribe(
      (data) => {
        this.reviews = data.reviews;
      },
      (error) => {
        console.error('Error fetching reviews', error);
      }
    );
  }

  deleteMovie() {
    this.movieService.deleteMovie(this.movie.movie_id, this.movie.title).subscribe(
      (response) => {
        alert(`Successfully deleted movie with id: ${this.movie.movie_id}`);
        this.router.navigate(['']);
      },
      (error) => {
        console.error('Error deleting movie', error);
      }
    );
  }

  downloadFile() {
    this.cognitoService.getUsername().then(username => {
      if (!username) {
        return;
      }
      this.movieService.downloadMovie(username, this.movie.movie_id).subscribe(
        response => {
          console.log('Download history created successfully:', response);
          const link = document.createElement('a');
          link.style.display = 'none';
          link.href = this.movie.download_url;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        },
        error => {
          console.error('Error creating download history:', error);
        }
      );
    }).catch(error => {
      console.error('Error getting username:', error);
    });
  }

  openReviewDialog(): void{
    const dialogRef = this.dialog.open(MovieReviewDialogComponent, {
      width: '550px',
      data: {
        movieId: this.movie.movie_id
      }
      });
  }


}

