import { Component } from '@angular/core';
import {MatSliderModule} from "@angular/material/slider";
import {MatInputModule} from "@angular/material/input";
import {FormsModule} from "@angular/forms";
import {MatDialogActions, MatDialogModule, MatDialogRef} from "@angular/material/dialog";
import {MatSelectModule} from "@angular/material/select";
import {NgForOf} from "@angular/common";
import {MatButton} from "@angular/material/button";

@Component({
  selector: 'app-movie-review-dialog',
  standalone: true,
  imports: [
    MatSliderModule, MatInputModule, FormsModule, MatDialogModule, MatSelectModule, NgForOf, MatDialogActions, MatButton
  ],
  templateUrl: './movie-review-dialog.component.html',
  styleUrl: './movie-review-dialog.component.css'
})
export class MovieReviewDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<MovieReviewDialogComponent>,
  ) {
  }
  onNoClick(): void {
    this.dialogRef.close();
  }
}
