import { Routes } from '@angular/router';
import {LoginComponent} from "./features/account-managing/login/login.component";
import {RegistrationComponent} from "./features/account-managing/registration-process/registration/registration.component";
import {RoleGuard} from "./core/guards/RoleGuard";
import {MovieDetailsComponent} from "./features/home/components/movies/movie-details/movie-details.component";
import {HomePageComponent} from "./features/home/components/home-page/home-page.component";
import {CreateMovieComponent} from "./features/home/components/movies/movie-creation/movie-creation.component";
import {MovieEditComponent} from "./features/home/components/movies/movie-edit/movie-edit.component";
import {SubscriptionsComponent} from "./features/home/components/subscriptions/subscriptions.component";

export const routes: Routes = [
  {
  path: 'login',
  component: LoginComponent
  },
  {
    path: 'registration',
    component: RegistrationComponent
  },
  {
    path: '',
    component: HomePageComponent
  },
  {
    path: 'movies/:id/:title',
    component: MovieDetailsComponent
  },
  {
    path: 'create-movie',
    component: CreateMovieComponent
  },
  {
    path: 'edit-movie/:id/:title',
    component: MovieEditComponent
  },
  {
    path: 'subscriptions',
    component: SubscriptionsComponent
  },
]
