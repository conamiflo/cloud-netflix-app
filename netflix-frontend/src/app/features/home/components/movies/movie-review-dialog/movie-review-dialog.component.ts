import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {ReviewService} from "../../../../../core/services/review/review.service";
import {CognitoService} from "../../../../../core/services/cognito/cognito.service";
import {MatOption} from "@angular/material/core";
import {MatFormField, MatLabel} from "@angular/material/form-field";
import {NgFor} from "@angular/common";
import {MatSelect} from "@angular/material/select";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-movie-review-dialog',
  templateUrl: './movie-review-dialog.component.html',
  standalone: true,
  imports: [MatOption, MatFormField, NgFor, MatSelect, MatLabel, FormsModule],
  styleUrls: ['./movie-review-dialog.component.css']
})
export class MovieReviewDialogComponent {
  movieId: string;
  reviewValue: number;

  constructor(
    public dialogRef: MatDialogRef<MovieReviewDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private reviewService: ReviewService,
    private cognitoService: CognitoService
  ) {
    this.movieId = data.movieId;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  async submitReview(): Promise<void> {
    try {
      const userInfo = await this.cognitoService.getUser();
      const username = userInfo.username;

      (await this.reviewService.submitReview(username, this.movieId, this.reviewValue)).subscribe(
          (response: any) => {
          console.log('Review submitted successfully:', response);
          alert('Review submitted successfully!');
          this.dialogRef.close();
        },
          (error: any) => {
          console.error('Error submitting review:', error);
          alert('Failed to submit review.');
        }
      );
    } catch (error) {
      console.error('Error getting username:', error);
    }
  }
}
