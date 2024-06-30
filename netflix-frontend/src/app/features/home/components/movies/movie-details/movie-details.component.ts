import { Component, OnInit } from '@angular/core';
import { addIcons} from 'ionicons';
import {IonIcon} from '@ionic/angular/standalone'
import { cameraOutline, playCircle, shareSocial, play, downloadOutline, chevronUp ,calendarOutline,timeOutline,star,send} from 'ionicons/icons';
import {MovieReviewComponent} from "../movie-review/movie-review.component";
import {MovieCardComponent} from "../movie-card/movie-card.component";
import {MovieReviewDialogComponent} from "../movie-review-dialog/movie-review-dialog.component";
import {MatDialog} from "@angular/material/dialog";
import {MatFormField, MatLabel} from "@angular/material/form-field";
import {ActivatedRoute} from "@angular/router";
import {MovieService} from "../../../../../core/services/movie/movie.service";
import {NgFor} from "@angular/common";

@Component({
  selector: 'app-movie-details',
  standalone: true,
  imports: [IonIcon, MovieReviewComponent, MovieCardComponent,MatLabel,MatFormField,NgFor],
  templateUrl: './movie-details.component.html',
  styleUrl: './movie-details.component.css'
})
export class MovieDetailsComponent{
  constructor(public dialog: MatDialog,
              private route: ActivatedRoute,
              private movieService: MovieService,) {
    addIcons({ cameraOutline, playCircle, shareSocial, play, downloadOutline, chevronUp,calendarOutline,timeOutline,star,send});
  }
  movie: any;

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const movieId = params.get('id');
      const movieTitle = params.get('title');
      console.log(movieId);
      console.log(movieTitle)

      if (movieId && movieTitle) {
        this.movieService.getMovieByIdAndTitle(movieId, movieTitle).subscribe(
          (data) => {
            this.movie = data;
            console.log(this.movie)
          },
          (error) => {
            console.error('Error fetching movie data', error);
          }
        );
      }
    });
  }


  openReviewDialog(): void{
    const dialogRef = this.dialog.open(MovieReviewDialogComponent, {
      width: '550px'
      });
  }
}

