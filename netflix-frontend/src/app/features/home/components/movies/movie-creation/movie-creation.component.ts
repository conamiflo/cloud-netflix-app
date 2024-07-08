import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import {MovieService} from "../../../../../core/services/movie/movie.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-create-movie',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './movie-creation.component.html',
  styleUrls: ['./movie-creation.component.scss']
})
export class CreateMovieComponent implements OnInit {
  createMovieForm: FormGroup;
  formData: any = {};

  constructor(private fb: FormBuilder,private movieService: MovieService, private router: Router) {
    this.createMovieForm = this.fb.group({
      title: ['', [Validators.required, Validators.pattern(/^[^_]*$/)]], // Exclude underscore
      genres: ['', [Validators.required, Validators.pattern(/^[^_]*$/)]],
      actors: ['', [Validators.required, Validators.pattern(/^[^_]*$/)]],
      description: ['', [Validators.required, Validators.pattern(/^[^_]*$/)]],
      directors: ['', [Validators.required, Validators.pattern(/^[^_]*$/)]],
      movieFile: [null, Validators.required],
      series: [''],
      movie: [null]
    });
  }

  ngOnInit(): void {
  }

  async onSubmit(): Promise<void> {
    if (this.createMovieForm.valid) {
      this.formData.title = this.createMovieForm.value.title;
      this.formData.genres = this.createMovieForm.value.genres.split(',').map((genre: string) => genre.trim());
      this.formData.actors = this.createMovieForm.value.actors.split(',').map((actor: string) => actor.trim());
      this.formData.description = this.createMovieForm.value.description;
      this.formData.directors = this.createMovieForm.value.directors.split(',').map((director: string) => director.trim());
      this.formData.movieFile = this.createMovieForm.value.movieFile;
      this.formData.series = this.createMovieForm.value.series;
      this.formData.movie = this.createMovieForm.value.movie;

      (await this.movieService.createMovie(this.formData)).subscribe(
        async response => {
          alert('Movie created successfully!');
          (await this.movieService.startTranscoding(response['movie_id'])).subscribe(
            response => {
              console.log('Movie transcoded successfully!');
              this.router.navigate(['']);
            },
            error => {
              alert('Failed to transcode movie.');
            }
          );
        },
        error => {
          alert('Failed to create movie.');
        }
      );

      // (await this.movieService.startTranscoding('1')).subscribe(
      //   response => {
      //   },
      //   error => {
      //     alert('Failed to transcode movie.');
      //   }
      // );


    } else {
      alert('Form is not valid. All fields are required and a file must be uploaded.');
    }
  }

  onFileChange(event: any): void {
    const file = event?.target?.files?.[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      this.createMovieForm.patchValue({
        movie: (reader.result as string).split(",")[1]
      });
    };
  }
}
