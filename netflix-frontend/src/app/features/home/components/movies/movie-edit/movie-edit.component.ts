import { Component } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {ActivatedRoute, Router} from "@angular/router";
import {MovieService} from "../../../../../core/services/movie/movie.service";

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
  editMovieForm: FormGroup;
  movie: any;
  formData: any = {};

  constructor(
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private movieService: MovieService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.editMovieForm = this.formBuilder.group({
      title: ['', Validators.required],
      genres: ['', Validators.required],
      actors: ['', Validators.required],
      description: ['', Validators.required],
      directors: ['', Validators.required],
      movieFile: [null],
      series: ['', Validators.required],
      movie: [null]
    });
    this.route.paramMap.subscribe(params => {
      const movieId = params.get('id');
      const movieTitle = params.get('title');
      if (movieId && movieTitle) {
        this.getMovieDetails(movieId, movieTitle);
      }
    });
  }

  getMovieDetails(movieId: string, movieTitle: string) {
    this.movieService.getMovieByIdAndTitle(movieId, movieTitle).subscribe(
      (data) => {
        this.movie = data;
        this.editMovieForm.patchValue({
          title: data.title,
          genres: data.genres.join(', '),
          actors: data.actors.join(', '),
          description: data.description,
          directors: data.directors.join(', '),
          series: data.series
        });
      },
      (error) => {
        console.error('Error fetching movie details', error);
      }
    );
  }

  editMovie() {
    if (this.editMovieForm.valid) {
      this.formData.title = this.editMovieForm.value.title;
      this.formData.genres = this.editMovieForm.value.genres.split(',').map((genre: string) => genre.trim());
      this.formData.actors = this.editMovieForm.value.actors.split(',').map((actor: string) => actor.trim());
      this.formData.description = this.editMovieForm.value.description;
      this.formData.directors = this.editMovieForm.value.directors.split(',').map((director: string) => director.trim());
      this.formData.movieFile = this.editMovieForm.value.movieFile;
      this.formData.series = this.editMovieForm.value.series;
      this.formData.movie = this.editMovieForm.value.movie;
      console.log(this.formData)
      this.movieService.editMovie(this.movie.movie_id,this.formData).subscribe(
        response => {
          alert('Movie edited successfully!');
          this.router.navigate([`movies/${this.movie.movie_id}/${this.formData.title}`]);
        },
        error => {
          alert('Failed to edit movie.');
        }
      );
    } else {
      alert('Form is not valid. Please fill out all required fields.');
    }
  }

  onFileChange(event: any): void {
    const file = event?.target?.files?.[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      this.editMovieForm.patchValue({
        movie: (reader.result as string).split(",")[1]
      });
    };

  }

}
