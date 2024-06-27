import { Component, OnInit } from '@angular/core';
import { addIcons} from 'ionicons';
import {IonIcon} from '@ionic/angular/standalone'
import { cameraOutline, playCircle, shareSocial, play, downloadOutline, chevronUp ,calendarOutline,timeOutline,star} from 'ionicons/icons';
import {MovieReviewComponent} from "../movie-review/movie-review.component";
import {MovieCardComponent} from "../movie-card/movie-card.component";
import {MovieReviewDialogComponent} from "../movie-review-dialog/movie-review-dialog.component";
import {MatDialog} from "@angular/material/dialog";
import {MatFormField, MatLabel} from "@angular/material/form-field";

@Component({
  selector: 'app-movie-details',
  standalone: true,
  imports: [IonIcon, MovieReviewComponent, MovieCardComponent,MatLabel,MatFormField],
  templateUrl: './movie-details.component.html',
  styleUrl: './movie-details.component.css'
})
export class MovieDetailsComponent{
  constructor(public dialog: MatDialog) {
    addIcons({ cameraOutline, playCircle, shareSocial, play, downloadOutline, chevronUp,calendarOutline,timeOutline,star});
  }

  openReviewDialog(): void{
    const dialogRef = this.dialog.open(MovieReviewDialogComponent, {
      width: '550px'
      });
  }
}

