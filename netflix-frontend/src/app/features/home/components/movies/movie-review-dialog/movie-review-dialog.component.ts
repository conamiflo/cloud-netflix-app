import { Component } from '@angular/core';
import {MatFormField} from "@angular/material/form-field";
import {MatOption} from "@angular/material/core";
import {MatSelect} from "@angular/material/select";

@Component({
  selector: 'app-movie-review-dialog',
  standalone: true,
  imports: [
    MatFormField,
    MatOption,
    MatSelect
  ],
  templateUrl: './movie-review-dialog.component.html',
  styleUrl: './movie-review-dialog.component.css'
})
export class MovieReviewDialogComponent {

}
