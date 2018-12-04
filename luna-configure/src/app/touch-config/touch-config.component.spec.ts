import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TouchConfigComponent } from './touch-config.component';

describe('TouchConfigComponent', () => {
  let component: TouchConfigComponent;
  let fixture: ComponentFixture<TouchConfigComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TouchConfigComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TouchConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
