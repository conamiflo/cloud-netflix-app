import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

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

  constructor(private fb: FormBuilder) {
    this.createMovieForm = this.fb.group({
      title: ['', Validators.required],
      genres: ['', Validators.required],
      actors: ['', Validators.required],
      description: ['', Validators.required],
      directors: ['', Validators.required],
      movie: [null, Validators.required],
      movieBase64: [null]
    });
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    if (this.createMovieForm.valid) {
      this.formData.title = this.createMovieForm.value.title;
      this.formData.genres = this.createMovieForm.value.genres;
      this.formData.actors = this.createMovieForm.value.actors;
      this.formData.description = this.createMovieForm.value.description;
      this.formData.directors = this.createMovieForm.value.directors;
      this.formData.movie = this.createMovieForm.value.movie;
      this.formData.movieBase64 = this.createMovieForm.value.movieBase64;

      console.log('Form data:', this.formData);

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
        movieBase64: (reader.result as string).split(",")[1]
      });
      console.log((reader.result as string).split(",")[1])
    };
  }
}
