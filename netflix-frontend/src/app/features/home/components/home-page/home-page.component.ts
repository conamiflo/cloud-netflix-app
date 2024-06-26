import { Component } from '@angular/core';
import {MovieCardComponent} from "../movies/movie-card/movie-card.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [MovieCardComponent],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {

}
