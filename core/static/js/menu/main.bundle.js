webpackJsonp(["main"],{

/***/ "../../../../../src/$$_lazy_route_resource lazy recursive":
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "../../../../../src/$$_lazy_route_resource lazy recursive";

/***/ }),

/***/ "../../../../../src/app/app-routing.module.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppRoutingModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__quiz_quiz_component__ = __webpack_require__("../../../../../src/app/quiz/quiz.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_common__ = __webpack_require__("../../../common/esm5/common.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__quiz_creator_quiz_creator_component__ = __webpack_require__("../../../../../src/app/quiz-creator/quiz-creator.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__quiz_role_creator_quiz_role_creator_component__ = __webpack_require__("../../../../../src/app/quiz-role-creator/quiz-role-creator.component.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};






var routes = [
    { path: '', component: __WEBPACK_IMPORTED_MODULE_2__quiz_quiz_component__["a" /* QuizComponent */] },
    { path: 'create', component: __WEBPACK_IMPORTED_MODULE_4__quiz_creator_quiz_creator_component__["a" /* QuizCreatorComponent */] },
    { path: 'create/:role', component: __WEBPACK_IMPORTED_MODULE_5__quiz_role_creator_quiz_role_creator_component__["a" /* QuizRoleCreatorComponent */] },
];
var AppRoutingModule = (function () {
    function AppRoutingModule() {
    }
    AppRoutingModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["I" /* NgModule */])({
            imports: [__WEBPACK_IMPORTED_MODULE_1__angular_router__["c" /* RouterModule */].forRoot(routes)],
            exports: [__WEBPACK_IMPORTED_MODULE_1__angular_router__["c" /* RouterModule */]],
            providers: [{ provide: __WEBPACK_IMPORTED_MODULE_3__angular_common__["a" /* APP_BASE_HREF */], useValue: '/menu/test' }]
        })
    ], AppRoutingModule);
    return AppRoutingModule;
}());



/***/ }),

/***/ "../../../../../src/app/app.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "/* AppComponent's private CSS styles */\nh1 {\n  font-size: 1.2em;\n  color: #999;\n  margin-bottom: 0;\n}\nh2 {\n  font-size: 2em;\n  margin-top: 0;\n  padding-top: 0;\n}\nnav a {\n  padding: 5px 10px;\n  text-decoration: none;\n  margin-top: 10px;\n  display: inline-block;\n  background-color: #eee;\n  border-radius: 4px;\n}\nnav a:visited, a:link {\n  color: #607D8B;\n}\nnav a:hover {\n  color: #039be5;\n  background-color: #CFD8DC;\n}\nnav a.active {\n  color: #039be5;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/app.component.html":
/***/ (function(module, exports) {

module.exports = "<router-outlet></router-outlet>\n\n"

/***/ }),

/***/ "../../../../../src/app/app.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};

var AppComponent = (function () {
    function AppComponent() {
    }
    AppComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-root',
            template: __webpack_require__("../../../../../src/app/app.component.html"),
            styles: [__webpack_require__("../../../../../src/app/app.component.css")]
        })
    ], AppComponent);
    return AppComponent;
}());



/***/ }),

/***/ "../../../../../src/app/app.module.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__ = __webpack_require__("../../../platform-browser/esm5/platform-browser.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_component__ = __webpack_require__("../../../../../src/app/app.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__quiz_quiz_component__ = __webpack_require__("../../../../../src/app/quiz/quiz.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__app_routing_module__ = __webpack_require__("../../../../../src/app/app-routing.module.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__quiz_service__ = __webpack_require__("../../../../../src/app/quiz.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__in_memory_data_service__ = __webpack_require__("../../../../../src/app/in-memory-data.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__angular_forms__ = __webpack_require__("../../../forms/esm5/forms.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__quiz_review_quiz_review_component__ = __webpack_require__("../../../../../src/app/quiz-review/quiz-review.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10_ngx_cookie_service__ = __webpack_require__("../../../../ngx-cookie-service/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_11__quiz_submit_quiz_submit_component__ = __webpack_require__("../../../../../src/app/quiz-submit/quiz-submit.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_12__quiz_creator_quiz_creator_component__ = __webpack_require__("../../../../../src/app/quiz-creator/quiz-creator.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_13__question_details_question_details_component__ = __webpack_require__("../../../../../src/app/question-details/question-details.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_14__quiz_role_creator_quiz_role_creator_component__ = __webpack_require__("../../../../../src/app/quiz-role-creator/quiz-role-creator.component.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};















var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__app_component__["a" /* AppComponent */],
                __WEBPACK_IMPORTED_MODULE_3__quiz_quiz_component__["a" /* QuizComponent */],
                __WEBPACK_IMPORTED_MODULE_9__quiz_review_quiz_review_component__["a" /* QuizReviewComponent */],
                __WEBPACK_IMPORTED_MODULE_11__quiz_submit_quiz_submit_component__["a" /* QuizSubmitComponent */],
                __WEBPACK_IMPORTED_MODULE_12__quiz_creator_quiz_creator_component__["a" /* QuizCreatorComponent */],
                __WEBPACK_IMPORTED_MODULE_13__question_details_question_details_component__["a" /* QuestionDetailsComponent */],
                __WEBPACK_IMPORTED_MODULE_14__quiz_role_creator_quiz_role_creator_component__["a" /* QuizRoleCreatorComponent */],
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__["a" /* BrowserModule */],
                __WEBPACK_IMPORTED_MODULE_8__angular_forms__["a" /* FormsModule */],
                __WEBPACK_IMPORTED_MODULE_4__app_routing_module__["a" /* AppRoutingModule */],
                __WEBPACK_IMPORTED_MODULE_6__angular_common_http__["b" /* HttpClientModule */],
            ],
            providers: [__WEBPACK_IMPORTED_MODULE_5__quiz_service__["a" /* QuizService */], __WEBPACK_IMPORTED_MODULE_7__in_memory_data_service__["a" /* InMemoryDataService */], __WEBPACK_IMPORTED_MODULE_10_ngx_cookie_service__["a" /* CookieService */]],
            bootstrap: [__WEBPACK_IMPORTED_MODULE_2__app_component__["a" /* AppComponent */]]
        })
    ], AppModule);
    return AppModule;
}());



/***/ }),

/***/ "../../../../../src/app/in-memory-data.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return InMemoryDataService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};

var InMemoryDataService = (function () {
    function InMemoryDataService() {
    }
    InMemoryDataService.prototype.createDb = function () {
        var test = [
            { id: 'get_quiz', is_preview: true, time_to_pass: 15, score_to_pass: 60, name: 'Waiters test',
                questions: this.createQuestions(10) },
            { id: 'get_specific_quiz', is_preview: true, time_to_pass: 15, score_to_pass: 60, name: 'Waiters test',
                questions: this.createQuestions(10) },
            { id: 'get_quizzes', business_name: 'cool-business',
                roles: [{ 'name': 'Waiter', 'imageUrl': 'https://png.icons8.com/metro/50/000000/waiter.png' },
                    { 'name': 'Bartender', 'imageUrl': 'https://png.icons8.com/metro/50/000000/waiter.png' },
                    { 'name': 'Cook', 'imageUrl': 'https://png.icons8.com/metro/50/000000/waiter.png' }] },
        ];
        return { test: test };
    };
    InMemoryDataService.prototype.createQuestions = function (num) {
        var questions = [];
        var drinks = { 0: 'Rum', 1: 'Tapioca', 2: 'Whiskey', 3: 'Vodka' };
        for (var i = 0; i < num; i++) {
            questions.push({ id: i, content: 'What is the best ' + drinks[i % 4],
                answers: this.createAnswers(i), answered: true });
        }
        return questions;
    };
    InMemoryDataService.prototype.createAnswers = function (num) {
        var answers = [];
        for (var i = 0; i < 4; i++) {
            answers.push({ id: i, questionId: 1, is_correct: i == 1,
                content: 'koko_' + (num + 1) + '_' + (i + 1), selected: false });
        }
        return answers;
    };
    InMemoryDataService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* Injectable */])()
    ], InMemoryDataService);
    return InMemoryDataService;
}());



/***/ }),

/***/ "../../../../../src/app/models/answer.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Answer; });
var Answer = (function () {
    function Answer() {
        this.selected = false;
    }
    Answer.createFrom = function (data) {
        var answer = new Answer();
        data = data || {};
        answer.id = data.id;
        answer.questionId = data.question;
        answer.name = data.content;
        answer.isAnswer = data.is_correct;
        answer.selected = false;
        return answer;
    };
    return Answer;
}());



/***/ }),

/***/ "../../../../../src/app/models/question.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Question; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__answer__ = __webpack_require__("../../../../../src/app/models/answer.ts");

var Question = (function () {
    function Question() {
        this.answered = false;
    }
    Question.createFrom = function (data) {
        var question = new Question();
        data = data || {};
        question.answers = [];
        question.id = data.id;
        question.name = data.content;
        if (data.answers) {
            data.answers.forEach(function (a) {
                question.answers.push(__WEBPACK_IMPORTED_MODULE_0__answer__["a" /* Answer */].createFrom(a));
            });
        }
        else {
            question.answers = [];
        }
        return question;
    };
    return Question;
}());



/***/ }),

/***/ "../../../../../src/app/models/quiz.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Quiz; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__question__ = __webpack_require__("../../../../../src/app/models/question.ts");

var Quiz = (function () {
    function Quiz() {
    }
    Quiz.createFrom = function (data) {
        var quiz = new Quiz();
        if (data) {
            quiz.id = data.id;
            quiz.name = data.name;
            quiz.scoreToPass = data.score_to_pass;
            quiz.time = data.time_to_pass;
            quiz.isPreview = data.is_preview;
            quiz.questions = [];
            if (data.questions) {
                data.questions.forEach(function (q) {
                    quiz.questions.push(__WEBPACK_IMPORTED_MODULE_0__question__["a" /* Question */].createFrom(q));
                });
            }
            else {
                quiz.questions = [];
            }
        }
        return quiz;
    };
    return Quiz;
}());



/***/ }),

/***/ "../../../../../src/app/question-details/question-details.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".panel {\n  border: 1px solid rgb(96, 125, 139);\n  /*border-radius:0 !important;*/\n  transition: box-shadow 0.5s;\n}\n.panel:hover {\n  box-shadow: 5px 0px 40px rgba(0,0,0, .2);\n}\n.panel-footer .btn:hover {\n  border: 1px solid lightsteelblue;\n  background-color: #fff !important;\n  color: rgb(96, 125, 139);\n}\n.panel-heading {\n  color: #fff !important;\n  background-color: rgb(96, 125, 139) !important;\n  padding: 8px;\n  border-bottom: 1px solid transparent;\n}\n.panel-footer {\n  background-color: white !important;\n}\n.panel-footer h3 {\n  font-size: 32px;\n}\n.panel-footer h4 {\n  color: #aaa;\n  font-size: 14px;\n}\n.panel-footer .btn {\n  margin: 15px 0;\n  background-color: rgb(96, 125, 139);\n  color: #fff;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/question-details/question-details.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"panel panel-default\">\n  <div class=\"panel-heading\">\n    <h5 class=\"panel-title\" style=\"display: inline\">{{ question.name }}</h5>\n  </div>\n  <div class=\"panel-body\">\n    <div class=\"row\">\n      <div class=\"col-sm-3\" *ngFor=\"let answer of question.answers\">\n        <h5>\n          <span class=\"badge\"\n                [ngClass]=\"{'badge-danger': !answer.isAnswer, 'badge-success': answer.isAnswer}\">\n            {{answer.name}}\n          </span>\n        </h5>\n      </div>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/question-details/question-details.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuestionDetailsComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__models_question__ = __webpack_require__("../../../../../src/app/models/question.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var QuestionDetailsComponent = (function () {
    function QuestionDetailsComponent() {
    }
    QuestionDetailsComponent.prototype.ngOnInit = function () {
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["D" /* Input */])(),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_1__models_question__["a" /* Question */])
    ], QuestionDetailsComponent.prototype, "question", void 0);
    QuestionDetailsComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-question-details',
            template: __webpack_require__("../../../../../src/app/question-details/question-details.component.html"),
            styles: [__webpack_require__("../../../../../src/app/question-details/question-details.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], QuestionDetailsComponent);
    return QuestionDetailsComponent;
}());



/***/ }),

/***/ "../../../../../src/app/quiz-creator/quiz-creator.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".panel {\n  border: 1px solid rgb(96, 125, 139);\n  border-radius:0 !important;\n  transition: box-shadow 0.5s;\n}\n.panel:hover {\n  box-shadow: 5px 0px 40px rgba(0,0,0, .2);\n}\n.panel-footer .btn:hover {\n  border: 1px solid lightsteelblue;\n  background-color: #fff !important;\n  color: rgb(96, 125, 139);\n}\n.panel-heading {\n  color: #fff !important;\n  background-color: rgb(96, 125, 139) !important;\n  padding: 25px;\n  border-bottom: 1px solid transparent;\n  border-top-left-radius: 0px;\n  border-top-right-radius: 0px;\n  border-bottom-left-radius: 0px;\n  border-bottom-right-radius: 0px;\n}\n.panel-footer {\n  background-color: white !important;\n}\n.panel-footer h3 {\n  font-size: 32px;\n}\n.panel-footer h4 {\n  color: #aaa;\n  font-size: 14px;\n}\n.panel-footer .btn {\n  margin: 15px 0;\n  background-color: rgb(96, 125, 139);\n  color: #fff;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/quiz-creator/quiz-creator.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"jumbotron\">\n  <h2>{{businessName}} Quiz Creator</h2>\n</div>\n\n<div class=\"container-fluid\" *ngIf=\"roles\">\n  <div class=\"text-center\">\n    <h4>Pick role</h4>\n  </div>\n  <div class=\"row\">\n    <div class=\"col-sm-4 col-xs-12\" *ngFor=\"let role of roles\">\n      <div class=\"panel panel-default text-center\">\n        <div class=\"panel-heading\">\n          <h1>{{role.name}}</h1>\n        </div>\n        <div class=\"panel-body\">\n          <img [src]=\"role.imageUrl\">\n        </div>\n        <div class=\"panel-footer\">\n          <button class=\"btn btn-primary\" (click)=\"gotoQuiz(role.name)\">Create</button>\n        </div>\n      </div>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/quiz-creator/quiz-creator.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizCreatorComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__quiz_service__ = __webpack_require__("../../../../../src/app/quiz.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var QuizCreatorComponent = (function () {
    function QuizCreatorComponent(quizService, router) {
        this.quizService = quizService;
        this.router = router;
        this.businessName = '';
    }
    QuizCreatorComponent.prototype.ngOnInit = function () {
        this.getQuizzes();
    };
    QuizCreatorComponent.prototype.getQuizzes = function () {
        var _this = this;
        this.quizService.getQuizzes().subscribe(function (res) {
            _this.businessName = res['businessName'];
            _this.roles = res['roles'];
        }, function (err) {
            console.error("Error: " + JSON.stringify(err));
        });
    };
    QuizCreatorComponent.prototype.gotoQuiz = function (roleName) {
        console.log('gotoQuiz' + roleName);
        this.router.navigate(['create', roleName]);
    };
    QuizCreatorComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-quiz-creator',
            template: __webpack_require__("../../../../../src/app/quiz-creator/quiz-creator.component.html"),
            styles: [__webpack_require__("../../../../../src/app/quiz-creator/quiz-creator.component.css")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__quiz_service__["a" /* QuizService */], __WEBPACK_IMPORTED_MODULE_2__angular_router__["b" /* Router */]])
    ], QuizCreatorComponent);
    return QuizCreatorComponent;
}());



/***/ }),

/***/ "../../../../../src/app/quiz-review/quiz-review.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".answered {\n  background-color:lightskyblue;\n  border:1px solid lightskyblue;\n  margin:2px 0;\n  padding:12px;\n}\n\n.not-answered {\n  background-color:yellow;\n  border:1px solid #eae5a6;\n  margin:2px 0;\n  padding:12px;\n}\n\n.offset-sm-4 {\n  margin-bottom: 40px;\n}\n\n.submitRow {\n  margin-top: 30px;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/quiz-review/quiz-review.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"container\" *ngIf=\"!submitted\">\n  <div class=\"row\">\n    <div class=\"col-sm-4\" *ngFor=\"let question of quiz.questions; let index = index;\">\n      <div [ngClass]=\"{'answered': isAnswered(question), 'not-answered': !isAnswered(question)}\"\n           (click)=\"gotoQuestion(question.id)\">\n        {{index + 1}}. <strong>{{ question.name }}</strong> <hr>\n        Your answer: <i>{{ selectedAnswer(question) }}</i>\n      </div>\n    </div>\n  </div>\n  <div class=\"row submitRow\">\n    <div class=\"col-sm-4 offset-sm-4\">\n      <button class=\"btn btn-lg btn-primary\" [disabled]=\"quiz.isPreview\" (click)=\"submitQuiz()\">Submit</button> <br>\n        <small>Click on a question to view it</small>\n    </div>\n  </div>\n</div>\n\n<app-quiz-submit [quiz]=\"quiz\" [result]=\"submitResult\" *ngIf=\"submitted\"></app-quiz-submit>\n"

/***/ }),

/***/ "../../../../../src/app/quiz-review/quiz-review.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizReviewComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__models_quiz__ = __webpack_require__("../../../../../src/app/models/quiz.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__quiz_service__ = __webpack_require__("../../../../../src/app/quiz.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var QuizReviewComponent = (function () {
    function QuizReviewComponent(quizService) {
        this.quizService = quizService;
        this.showQuestion = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["v" /* EventEmitter */]();
        this.submitted = false;
    }
    QuizReviewComponent.prototype.ngOnInit = function () {
        console.log(JSON.stringify(this.quiz.questions[0].answers[0]));
    };
    QuizReviewComponent.prototype.isAnswered = function (question) {
        return !!question.answers.find(function (x) { return x.selected; });
    };
    ;
    QuizReviewComponent.prototype.selectedAnswer = function (question) {
        var name;
        question.answers.forEach(function (a) {
            if (a.selected) {
                name = a.name;
            }
        });
        return name ? name : "not answered";
    };
    QuizReviewComponent.prototype.gotoQuestion = function (questionId) {
        console.log(questionId);
        this.showQuestion.emit(questionId);
    };
    QuizReviewComponent.prototype.submitQuiz = function () {
        var _this = this;
        this.quizService.submitQuiz(this.quiz).subscribe(function (res) {
            _this.submitted = true;
            console.log('ok, res is: ' + JSON.stringify(res));
            _this.submitResult = res;
            setTimeout(window.location.reload.bind(window.location), 3000);
        }, function (err) {
            console.error("Error: " + err.message);
        });
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["D" /* Input */])(),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_1__models_quiz__["a" /* Quiz */])
    ], QuizReviewComponent.prototype, "quiz", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["P" /* Output */])(),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_0__angular_core__["v" /* EventEmitter */])
    ], QuizReviewComponent.prototype, "showQuestion", void 0);
    QuizReviewComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-quiz-review',
            template: __webpack_require__("../../../../../src/app/quiz-review/quiz-review.component.html"),
            styles: [__webpack_require__("../../../../../src/app/quiz-review/quiz-review.component.css")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__quiz_service__["a" /* QuizService */]])
    ], QuizReviewComponent);
    return QuizReviewComponent;
}());



/***/ }),

/***/ "../../../../../src/app/quiz-role-creator/quiz-role-creator.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".container {\n  margin-top: 30px;\n}\n\n\n.col-md-6 {\n  margin-bottom: 20px;\n}\n\n.newQuestion {\n  margin-top: 20px;\n}\n\n#questionAddHeader {\n  text-align: center;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/quiz-role-creator/quiz-role-creator.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"container\" *ngIf=\"quiz\">\n  <div class=\"page-header\"><h1>Create {{role}} menu test</h1></div>\n  <div class=\"jumbotron\">\n    <div class=\"row\">\n      <div class=\"col-sm-8\">\n        <h3>{{quiz.name}} - Basic settings</h3>\n        <form class=\"form-horizontal\">\n          <div class=\"form-group row\">\n            <label for=\"quizName\" class=\"col-sm-4 col-form-label\">Name: </label>\n            <div class=\"col-sm-6\">\n              <input type=\"text\" id=\"quizName\" [(ngModel)]=\"quiz.name\" class=\"form-control\" name=\"quizName\"/>\n            </div>\n          </div>\n          <div class=\"form-group row\">\n            <label for=\"quizMinTime\" class=\"col-sm-4 col-form-label\">Minimum score: </label>\n            <div class=\"col-sm-3\">\n              <input type=\"text\" id=\"quizMinTime\" [(ngModel)]=\"quiz.scoreToPass\" class=\"form-control\"\n                     name=\"quizMinTime\"/>\n            </div>\n          </div>\n          <div class=\"form-group row\">\n            <label for=\"quizMinScore\" class=\"col-sm-4 col-form-label\">Maximum time:</label>\n            <div class=\"col-sm-3\">\n              <input type=\"text\" id=\"quizMinScore\" [(ngModel)]=\"quiz.time\" class=\"form-control\" name=\"quizMinScore\"/>\n            </div>\n          </div>\n          <div class=\"form-group row\">\n            <div class=\"col-sm-4 offset-sm-4\">\n              <button class=\"btn btn-lg btn-primary\">Save</button>\n            </div>\n          </div>\n        </form>\n      </div>\n    </div>\n\n    <div class=\"row newQuestion\" *ngIf=\"newQuestion\">\n      <div class=\"col-sm-10\">\n        <h3 id=\"questionAddHeader\">Add/Edit Question</h3>\n        <form class=\"form-horizontal\">\n          <div class=\"form-group row\">\n            <label for=\"newQuestionName\" class=\"col-sm-2 col-form-label\">Question:</label>\n            <div class=\"col-sm-9\">\n              <input id=\"newQuestionName\" type=\"text\" [(ngModel)]=\"newQuestion.name\"\n                     class=\"form-control\" name=\"newQuestion\"/>\n            </div>\n            <div class=\"col-sm-1\">\n              <strong>#{{newQuestion.id}}</strong>\n            </div>\n          </div>\n\n          <div class=\"form-group row\" *ngFor=\"let a of this.newQuestion.answers; let i=index;\">\n            <label for=\"newAnswer{{i}}\" class=\"col-sm-2 col-form-label\">Answer {{i+1}} (#{{a.id}}): </label>\n            <div class=\"col-sm-8\">\n              <input type=\"text\" id=\"newAnswer{{i}}\" [(ngModel)]=\"a.name\"\n                     class=\"form-control\" name=\"newQuestionName{{i}}\"/>\n            </div>\n            <label for=\"newAnswer{{i}}-correct\" class=\"col-sm-1 col-form-label\">correct:</label>\n            <div class=\"col-sm-1\">\n              <input type=\"checkbox\" id=\"newAnswer{{i}}-correct\" [(ngModel)]=\"a.isAnswer\"\n                     class=\"form-control\" name=\"newQuestionIsCorrect-{{i}}\"/>\n            </div>\n          </div>\n\n          <div class=\"form-group row\">\n            <div class=\"col-sm-4 offset-sm-4\">\n              <button class=\"btn btn-lg btn-primary\">Save</button>\n            </div>\n          </div>\n        </form>\n      </div>\n    </div>\n  </div>\n</div>\n\n<div class=\"container\" *ngIf=\"quiz\">\n  <div class=\"row\" style=\"margin-top: 20px\">\n    <div class=\"col-md-6\" *ngFor=\"let question of quiz.questions\">\n      <app-question-details [question]=\"question\" (click)=\"setNewQuestion(question)\"></app-question-details>\n    </div>\n  </div>\n</div>\n\n<h2 *ngIf=\"errMsg\">{{errMsg}}</h2>\n"

/***/ }),

/***/ "../../../../../src/app/quiz-role-creator/quiz-role-creator.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizRoleCreatorComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__quiz_service__ = __webpack_require__("../../../../../src/app/quiz.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__models_quiz__ = __webpack_require__("../../../../../src/app/models/quiz.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__models_question__ = __webpack_require__("../../../../../src/app/models/question.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__models_answer__ = __webpack_require__("../../../../../src/app/models/answer.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};






var QuizRoleCreatorComponent = (function () {
    function QuizRoleCreatorComponent(route, quizService) {
        this.route = route;
        this.quizService = quizService;
        this.newQuestion = new __WEBPACK_IMPORTED_MODULE_4__models_question__["a" /* Question */]();
    }
    QuizRoleCreatorComponent.prototype.ngOnInit = function () {
        this.role = this.route.snapshot.paramMap.get('role');
        this.get_specific_quiz(this.role);
        this.set_answers_to_new_question();
    };
    QuizRoleCreatorComponent.prototype.get_specific_quiz = function (role) {
        var _this = this;
        this.quizService.getSpecificQuiz(role).subscribe(function (res) {
            _this.quiz = __WEBPACK_IMPORTED_MODULE_3__models_quiz__["a" /* Quiz */].createFrom(res);
        }, function (err) {
            if (err['status'] == 400) {
                console.error("Bad request Error: " + JSON.stringify(err));
                _this.errMsg = err.error;
            }
            else {
                console.error("Unexpected Error: " + JSON.stringify(err));
            }
        });
    };
    QuizRoleCreatorComponent.prototype.set_answers_to_new_question = function () {
        var answers = [];
        for (var i = 0; i < 4; i++) {
            var answer = new __WEBPACK_IMPORTED_MODULE_5__models_answer__["a" /* Answer */]();
            answer.isAnswer = false;
            answer.selected = false;
            answers.push(answer);
        }
        this.newQuestion.answers = answers;
    };
    QuizRoleCreatorComponent.prototype.setNewQuestion = function (ques) {
        this.newQuestion = ques;
    };
    QuizRoleCreatorComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-quiz-role-creator',
            template: __webpack_require__("../../../../../src/app/quiz-role-creator/quiz-role-creator.component.html"),
            styles: [__webpack_require__("../../../../../src/app/quiz-role-creator/quiz-role-creator.component.css")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */], __WEBPACK_IMPORTED_MODULE_2__quiz_service__["a" /* QuizService */]])
    ], QuizRoleCreatorComponent);
    return QuizRoleCreatorComponent;
}());



/***/ }),

/***/ "../../../../../src/app/quiz-submit/quiz-submit.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".correct {\n  background-color:lightgreen;\n  border:1px solid lightgreen;\n  margin:2px 0;\n  padding:12px;\n}\n\n.wrong, .not-answered {\n  background-color:red;\n  border:1px solid red;\n  margin:2px 0;\n  padding:12px;\n}\n\n.row {\n  margin-bottom: 30px;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/quiz-submit/quiz-submit.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"container\">\n  <div class=\"row\">\n    <div class=\"col-sm-4\" *ngFor=\"let question of quiz.questions; let index = index;\">\n      <div [ngClass]=\"{'correct': isCorrect(question), 'wrong': isCorrect(question) == false,\n       'not-answered': isCorrect(question) == null}\"\n           (click)=\"gotoQuestion(question.id)\">\n        {{index + 1}}. <strong>{{ question.name }}</strong> <hr>\n        Your answer: <i>{{ selectedAnswer(question) }}</i> <hr>\n        <p *ngIf=\"!isCorrect(question)\">correct answer is: <strong>{{correctAnswer(question)}}</strong></p>\n      </div>\n    </div>\n  </div>\n  <div class=\"row\">\n    <div class=\"col-sm-4 offset-sm-4\">\n      <h3 [ngStyle]=\"{'color':isPassed() ? 'green' : 'red'}\">\n        {{isPassed() ? 'You passed the menu test ! ' : 'You failed:('}}\n      </h3>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/quiz-submit/quiz-submit.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizSubmitComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__models_quiz__ = __webpack_require__("../../../../../src/app/models/quiz.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var QuizSubmitComponent = (function () {
    function QuizSubmitComponent() {
    }
    QuizSubmitComponent.prototype.ngOnInit = function () { };
    QuizSubmitComponent.prototype.isCorrect = function (question) {
        var correctAnswerId = this.result[question.id];
        var submittedAnswerId = this.getSubmittedAnswerId(question.answers);
        if (!submittedAnswerId) {
            return null;
        }
        return correctAnswerId == submittedAnswerId;
    };
    QuizSubmitComponent.prototype.getSubmittedAnswerId = function (answers) {
        var submittedId;
        answers.forEach(function (a) {
            if (a.selected) {
                submittedId = a.id;
            }
        });
        return submittedId ? submittedId : null;
    };
    QuizSubmitComponent.prototype.correctAnswer = function (question) {
        var correctAnswerId = this.result[question.id];
        var correctAnswerText;
        question.answers.forEach(function (a) {
            if (a.id == correctAnswerId) {
                correctAnswerText = a.name;
            }
        });
        return correctAnswerText;
    };
    QuizSubmitComponent.prototype.selectedAnswer = function (question) {
        var name;
        question.answers.forEach(function (a) {
            if (a.selected) {
                name = a.name;
            }
        });
        return name ? name : "not answered";
    };
    QuizSubmitComponent.prototype.isPassed = function () {
        return this.result['score'] >= this.quiz.scoreToPass;
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["D" /* Input */])(),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_1__models_quiz__["a" /* Quiz */])
    ], QuizSubmitComponent.prototype, "quiz", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["D" /* Input */])(),
        __metadata("design:type", Object)
    ], QuizSubmitComponent.prototype, "result", void 0);
    QuizSubmitComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-quiz-submit',
            template: __webpack_require__("../../../../../src/app/quiz-submit/quiz-submit.component.html"),
            styles: [__webpack_require__("../../../../../src/app/quiz-submit/quiz-submit.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], QuizSubmitComponent);
    return QuizSubmitComponent;
}());



/***/ }),

/***/ "../../../../../src/app/quiz.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_ngx_cookie_service__ = __webpack_require__("../../../../ngx-cookie-service/index.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var QuizService = (function () {
    function QuizService(http, cookieService) {
        this.http = http;
        this.cookieService = cookieService;
        this.httpOptions = {
            headers: new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]({ 'Content-Type': 'application/json', "X-CSRFToken": this.getCookie('csrftoken') })
        };
        this.menuUrl = 'menu/test'; // URL to web api
    }
    QuizService.prototype.getQuiz = function () {
        return this.http.get(this.menuUrl + '/get_quiz/');
    };
    QuizService.prototype.getSpecificQuiz = function (role) {
        return this.http.get(this.menuUrl + '/get_specific_quiz/' + role + '/');
    };
    QuizService.prototype.getQuestions = function () {
        return this.http.get(this.menuUrl + '/questions/');
    };
    QuizService.prototype.submitQuiz = function (quiz) {
        return this.http.post(this.menuUrl + '/submit/', quiz, this.httpOptions);
    };
    QuizService.prototype.getRetryStatus = function () {
        return this.http.get(this.menuUrl + '/ask_retry_quiz/');
    };
    QuizService.prototype.askForRetry = function () {
        return this.http.post(this.menuUrl + '/ask_retry_quiz/', {}, this.httpOptions);
    };
    QuizService.prototype.doRetry = function () {
        return this.http.post(this.menuUrl + '/retry_quiz/', {}, this.httpOptions);
    };
    QuizService.prototype.getCookie = function (key) {
        var cookie = this.cookieService.get(key);
        console.log('got ' + key + ' cookie: ' + cookie);
        return cookie;
    };
    QuizService.prototype.getQuizzes = function () {
        return this.http.get(this.menuUrl + '/get_quizzes/');
    };
    QuizService.prototype.create = function (quiz) {
    };
    QuizService.prototype.delete = function (id) {
    };
    QuizService.prototype.update = function (id, quiz) {
    };
    QuizService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */], __WEBPACK_IMPORTED_MODULE_2_ngx_cookie_service__["a" /* CookieService */]])
    ], QuizService);
    return QuizService;
}());



/***/ }),

/***/ "../../../../../src/app/quiz/quiz.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".jumbotron {\n  text-align: center;\n}\n\na:hover {\n  color:#607D8B;\n}\n\n.badge {\n  display: inline-block;\n  font-size: small;\n  color: white;\n  padding: 0.8em 0.7em 0 0.7em;\n  background-color: #607D8B;\n  line-height: 1em;\n  position: relative;\n  left: -1px;\n  top: -4px;\n  height: 1.8em;\n  min-width: 16px;\n  text-align: right;\n  margin-right: .8em;\n  border-radius: 4px 0 0 4px;\n}\n\n.button {\n  background-color: #eee;\n  border: none;\n  padding: 5px 10px;\n  border-radius: 4px;\n  cursor: pointer;\n  cursor: hand;\n  font-family: Arial;\n}\n\nbutton:hover {\n  background-color: #cfd8dc;\n}\n\nbutton.delete {\n  position: relative;\n  left: 194px;\n  top: -32px;\n  background-color: gray !important;\n  color: white;\n}\n\n.approved {\n color: green;\n}\n\n.rejected {\n  color: red;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/quiz/quiz.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"jumbotron\">\n  <div *ngIf=\"quiz\">\n    <h2>\n      <small *ngIf=\"quiz.isPreview\"><i>PREVIEW MODE OF:</i></small>\n      {{quiz.name}}\n    </h2>\n    <p >You'll have {{quiz.time}} minutes to solve it, minimum score is {{quiz.scoreToPass}}, Good luck</p>\n  </div>\n  <a href=\"/\" class=\"btn btn-primary\">Back to dashboard</a>\n</div>\n<div class=\"container\" *ngIf=\"mode == 'quiz' && quiz\">\n  <div class=\"badge badge-info\">Question {{currIndex + 1}} of {{quiz.questions.length}}.</div>\n  <h2>{{currIndex + 1}}. <span [innerHTML]=\"getCurrQuestion().name\"></span></h2>\n  <div class=\"row\">\n    <div class=\"col-md-6\" *ngFor=\"let answer of getCurrQuestion().answers\">\n      <div class=\"option\">\n        <label class=\"\" [attr.for]=\"answer.id\">\n          <input id=\"{{answer.id}}\" type=\"checkbox\" [(ngModel)]=\"answer.selected\"/>\n          {{answer.name}}\n        </label>\n      </div>\n    </div>\n  </div>\n  <hr>\n  <div class=\"text-sm-center\">\n    <button class=\"btn btn-default\" (click)=\"goTo(0);\">First</button>\n    <button class=\"btn btn-info\" (click)=\"goTo(currIndex - 1);\">Prev</button>\n    <button class=\"btn btn-primary\" (click)=\"goTo(currIndex + 1);\">Next</button>\n    <button class=\"btn btn-default\" (click)=\"goTo(count - 1);\">Last</button>\n  </div>\n  <div class=\"text-sm-center\">\n    <button class=\"btn btn-success\" (click)=\"mode = 'review'\" style=\"margin-top: 20px\">Review and submit</button>\n  </div>\n</div>\n\n<app-quiz-review [quiz]=\"quiz\" (showQuestion)=\"showQuestion($event)\"\n                 *ngIf=\"mode == 'review' && quiz\"></app-quiz-review>\n\n<div class=\"container\" *ngIf=\"errMsg\">\n  <h3>{{errMsg}}</h3>\n  <div *ngIf=\"retryStatus\" [ngClass]=\"{'approved': retryStatus  == 'Approved', 'rejected': retryStatus  == 'Rejected'}\">\n    <p *ngIf=\"retryStatus == 'non-exist'\">You can ask your manager to let you do this test again</p>\n    <p *ngIf=\"retryStatus == 'Pending'\">Your manager still has not responded to your request to retry</p>\n    <p *ngIf=\"retryStatus == 'Rejected'\">Unfortunately your manager rejected your request for retry :(</p>\n    <p *ngIf=\"retryStatus == 'Approved'\">Your manager approved your request to do this test again !</p>\n    <button class=\"btn btn-info\" *ngIf=\"retryStatus == 'non-exist'\" (click)=\"askRetry()\">\n      Ask your manager for retry</button>\n    <button class=\"btn btn-primary\" *ngIf=\"retryStatus == 'Approved'\" (click)=\"retryQuiz()\">\n      Retry quiz</button>\n  </div>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/quiz/quiz.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__models_quiz__ = __webpack_require__("../../../../../src/app/models/quiz.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__quiz_service__ = __webpack_require__("../../../../../src/app/quiz.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var QuizComponent = (function () {
    function QuizComponent(quizService) {
        this.quizService = quizService;
        this.currIndex = 0;
        this.roles = ['Waiter', 'Bartender', 'Cook'];
        this.mode = 'quiz';
    }
    QuizComponent.prototype.ngOnInit = function () {
        this.loadQuiz();
        // this.getRetryStatus();
    };
    QuizComponent.prototype.loadQuiz = function () {
        var _this = this;
        this.quizService.getQuiz().subscribe(function (res) {
            console.log(JSON.stringify(res));
            _this.quiz = __WEBPACK_IMPORTED_MODULE_1__models_quiz__["a" /* Quiz */].createFrom(res);
            console.log(JSON.stringify(_this.quiz));
            _this.count = _this.quiz.questions.length;
        }, function (err) {
            console.error("Error: " + JSON.stringify(err));
            if (err['status'] == 400) {
                _this.errMsg = err.error;
                _this.getRetryStatus();
            }
            else {
                _this.errMsg = "Unexpected error: " + err.error;
            }
        });
    };
    QuizComponent.prototype.getCurrQuestion = function () {
        return this.quiz.questions[this.currIndex];
    };
    QuizComponent.prototype.goTo = function (index) {
        if (index >= 0 && index < this.count) {
            this.currIndex = index;
        }
    };
    QuizComponent.prototype.showQuestion = function (id) {
        this.mode = 'quiz';
        this.goTo(id);
    };
    QuizComponent.prototype.getRetryStatus = function () {
        var _this = this;
        this.quizService.getRetryStatus().subscribe(function (res) {
            console.log('retry status is ' + JSON.stringify(res));
            _this.retryStatus = res.retry_status;
        }, function (err) {
            console.error('failed to get retry status: ' + JSON.stringify(err));
        });
    };
    QuizComponent.prototype.askRetry = function () {
        this.quizService.askForRetry().subscribe(function (res) {
            console.log('retry ask response is: ' + res.created);
            location.reload();
        }, function (err) {
            console.error('failed to ask for retry: ' + JSON.stringify(err));
        });
    };
    QuizComponent.prototype.retryQuiz = function () {
        this.quizService.doRetry().subscribe(function (res) {
            console.log('do retry response is: ' + res.created);
            location.reload();
        }, function (err) {
            console.error('failed to do retry: ' + JSON.stringify(err));
        });
    };
    QuizComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-quiz',
            template: __webpack_require__("../../../../../src/app/quiz/quiz.component.html"),
            styles: [__webpack_require__("../../../../../src/app/quiz/quiz.component.css")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__quiz_service__["a" /* QuizService */]])
    ], QuizComponent);
    return QuizComponent;
}());



/***/ }),

/***/ "../../../../../src/environments/environment.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return environment; });
// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.
var environment = {
    production: false
};


/***/ }),

/***/ "../../../../../src/main.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__ = __webpack_require__("../../../platform-browser-dynamic/esm5/platform-browser-dynamic.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_app_module__ = __webpack_require__("../../../../../src/app/app.module.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");




if (__WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].production) {
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_13" /* enableProdMode */])();
}
Object(__WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_2__app_app_module__["a" /* AppModule */])
    .catch(function (err) { return console.log(err); });


/***/ }),

/***/ 0:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("../../../../../src/main.ts");


/***/ })

},[0]);
//# sourceMappingURL=main.bundle.js.map