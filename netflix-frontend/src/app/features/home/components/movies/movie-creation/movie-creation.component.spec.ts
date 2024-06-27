import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MovieCreationComponent } from './movie-creation.component';

describe('MovieCreationComponent', () => {
  let component: MovieCreationComponent;
  let fixture: ComponentFixture<MovieCreationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MovieCreationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MovieCreationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
