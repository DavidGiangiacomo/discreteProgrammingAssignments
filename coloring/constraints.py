#!/usr/bin/python
# -*- coding: utf-8 -*-

class Constraint:
    def isFeasible(ds):
        return False

    def prune(ds):
        return False

    def unprune(ds):
        return False


class NotEqConstraint(Constraint):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.fixed = False

    def isFeasible(self, ds):
        da = ds.getValues(self.a)
        db = ds.getValues(self.b)
        for i in da:
            for j in db:
                if i != j:
                    return True
        return False

    def prune(self, ds):
        if self.fixed:
            return False
        change = False
        da = ds.getValues(self.a)
        db = ds.getValues(self.b)
        if (len(da) == 1 and da[0] in db):
            change = True
            db.remove(da[0])
        if (len(db) == 1 and db[0] in da):
            change = True
            da.remove(db[0])
        if len(da) == 1 and len(db) == 1:
            self.fixed = True
        return change
        
    def __str__( self ):
        return str(('NotEqConstraint',  self.a,  self.b))


class InferiorConstraint(Constraint):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def isFeasible(self, ds):
        da = ds.getValues(self.a)
        db = ds.getValues(self.b)
        for i in range(0, len(da)):
            for j in range(0, len(db)):
                if da[i] < da[j]:
                    return True
        return False

    def prune(self, ds):
        change = False
        da = ds.getValues(self.a)
        db = ds.getValues(self.b)
        maxDa = max(da)
        minDb = min(db)
        for i in range(0, len(da)):
            if da[i] >= minDb:
                change = True
                da.remove[da[i]]
        for i in range(0, len(db)):
            if db[i] <= maxDa:
                change = True
                db.remove[db[i]]
        return change

#TOFINISH
class SuperiorConstraint(Constraint):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def isFeasible(self, ds):
        da = ds.getValues(self.a)
        db = ds.getValues(self.b)
        for i in range(0, len(da)):
            for j in range(0, len(db)):
                if da[i] > da[j]:
                    return True
        return False

    def prune(self, ds):
        return False
        


class EqualConstantConstraint(Constraint):
    def __init__(self, a, c):
        self.a = a
        self.c = c

    def isFeasible(self, ds):
        da = ds.getValues(self.a)
        for i in range(0, len(da)):
            if da[i] == self.c:
                return True
        return False

    def prune(self, ds):
        da = ds.getValues(self.a)
        if len(da) == 1:
            return False
        tmp = da[0:len(da)]
        change= False
        for value in da:
            if value != self.c:
                change = True
                tmp.remove(value)
        if change:
            ds.setValues(self.a,  tmp)
        return change
                
class InferiorConstantConstraint(Constraint):
    def __init__(self, a, c):
        self.a = a
        self.c = c
        self.fixed = False

    def isFeasible(self, ds):
        da = ds.getValues(self.a)
        for i in da:
            if i < self.c:
                return True
        return False

    def prune(self, ds):
        if self.fixed:
            return False
        da = ds.getValues(self.a)
        tmp = da[0:len(da)]
        change= False
        for value in da:
            if value >= self.c:
                change = True
                tmp.remove(value)
        if change:
            self.fixed = True
            ds.setValues(self.a,  tmp)
        return change
        
    def __str__( self ):
        return str(('InferiorConstantConstraint',  self.a,  self.c))

#TOFINISH
class SuperiorConstantConstraint(Constraint):
    def __init__(self, a, c):
        self.a = a
        self.c = c

    def isFeasible(self, ds):
        da = ds.getValues(self.a)
        for i in range(0, len(da)):
            if da[i] > self.c:
                return True
        return False

    def prune(self, ds):
        return False

