import {Component, Input} from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import {MovieDTO} from "../../../../core/models/MovieDTO";

@Component({
  selector: 'app-movie-card',
  standalone: true,
  imports: [MatCardModule],
  templateUrl: './movie-card.component.html',
  styleUrl: './movie-card.component.css'
})

export class MovieCardComponent {

  @Input() movieDTO: MovieDTO;

}
