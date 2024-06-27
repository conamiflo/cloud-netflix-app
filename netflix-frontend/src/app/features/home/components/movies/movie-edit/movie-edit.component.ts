import { Component } from '@angular/core';
import {ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-movie-edit',
  standalone: true,
    imports: [
        ReactiveFormsModule
    ],
  templateUrl: './movie-edit.component.html',
  styleUrl: './movie-edit.component.scss'
})
export class MovieEditComponent {

}
