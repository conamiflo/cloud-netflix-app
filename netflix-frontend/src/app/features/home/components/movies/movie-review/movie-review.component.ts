import {Component, Input} from '@angular/core';
import {NgFor, NgIf} from "@angular/common";
import {IonIcon} from "@ionic/angular/standalone";
import {addIcons} from "ionicons";
import {star} from "ionicons/icons";

@Component({
  selector: 'app-movie-review',
  standalone: true,
  imports: [NgIf, NgFor, IonIcon],
  templateUrl: './movie-review.component.html',
  styleUrl: './movie-review.component.css'
})
export class MovieReviewComponent {
  @Input() review: any;
  constructor() {
    addIcons({star});
  }
}
