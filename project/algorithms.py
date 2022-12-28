from copy import deepcopy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])

        return solution


class BackTracking(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        solution = []
        iterationNumber = 0
        matrixValues = deepcopy(tiles)

        for i in range(len(matrixValues)):
            for j in range(len(matrixValues[0])):
                matrixValues[i][j] = 0

        domains = {var: [word for word in words] for var in variables}

        for var in variables:

            numberOfLetters = variables[var]

            startingDomainVar = []
            for word in domains[var]:
                if len(word) == numberOfLetters:
                    startingDomainVar.append(word)

            domains[var] = startingDomainVar

        self.backTrackIteration(iterationNumber, solution, domains, variables, matrixValues, tiles)

        return solution

    def backTrackIteration(self, iterationNumber, solution, domains, variables, matrixValues, tiles):

        if len(variables) == iterationNumber:
            return True

        v = list(variables.keys())[iterationNumber]

        currentDomain = domains[v]

        for val in domains[v]:
            coords = list(self.getVarCoordinates(v, variables[v], tiles))
            tupleCoords = coords[0]
            x = tupleCoords[0]
            xp = tupleCoords[0]
            y = tupleCoords[1]
            yp = tupleCoords[1]
            horVer = v[len(v) - 1]
            isHorizontal = (horVer == "h")

            if len(val) == variables[v] and self.checkIfValid(variables, tiles, matrixValues, x, y, isHorizontal, v, val):
                for i in range(0, len(val)):
                    matrixValues[xp][yp] = val[i]
                    if isHorizontal:
                        yp = yp + 1
                    else:
                        xp = xp + 1

                solution.append([v, currentDomain.index(val), domains])
                if self.backTrackIteration(iterationNumber + 1, solution, domains, variables, matrixValues, tiles):
                    return True

        solution.append([v, None, domains])
        return False

    def getVarCoordinates(self, variable, var_len, tiles):
        _i, _j = int(variable[:-1]) // len(tiles[0]), int(variable[:-1]) % len(tiles[0])
        return zip(range(_i, var_len + _i), [_j] * var_len) \
            if variable[-1] != 'h' \
            else zip([_i] * var_len, range(_j, var_len + _j))

    def checkIfValid(self, variables, tiles, matrixValues, x, y, isHorizontal, currV, val):
        newMatrix = deepcopy(matrixValues)
        xp = x
        yp = y

        for i in range(0, len(val)):
            newMatrix[xp][yp] = val[i]
            if isHorizontal:
                yp = yp + 1
            else:
                xp = xp + 1

        for v in variables:
            if v == currV:
                break
            coordsVar = list(self.getVarCoordinates(v, variables[v], tiles))
            tupleCoordsVar = coordsVar[0]
            xvar = tupleCoordsVar[0]
            yvar = tupleCoordsVar[1]
            horVerVar = v[len(v) - 1]
            isHorizontalVar = (horVerVar == "h")
            lengthVar = variables[v]

            xpVar = xvar
            ypVar = yvar

            for i in range(0, lengthVar):
                if newMatrix[xpVar][ypVar] != matrixValues[xpVar][ypVar]:
                    return False
                if isHorizontalVar:
                    ypVar = ypVar + 1
                else:
                    xpVar = xpVar + 1

        return True


class ForwardChecking(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        solution = []
        iterationNumber = 0
        matrixValues = deepcopy(tiles)

        for i in range(len(matrixValues)):
            for j in range(len(matrixValues[0])):
                matrixValues[i][j] = 0

        domains = {var: [word for word in words] for var in variables}

        for var in variables:
            numberOfLetters = variables[var]
            startingDomainVar = []
            for word in domains[var]:
                if len(word) == numberOfLetters:
                    startingDomainVar.append(word)

            domains[var] = startingDomainVar

        self.forwardCheckingIteration(iterationNumber, solution, domains, variables, matrixValues, tiles)

        return solution

    def forwardCheckingIteration(self, iterationNumber, solution, domains, variables, matrixValues, tiles):

        if len(variables) == iterationNumber:
            return True

        v = list(variables.keys())[iterationNumber]

        currentDomain = domains[v]

        for val in domains[v]:
            flag = False
            coords = list(self.getVarCoordinates(v, variables[v], tiles))
            tupleCoords = coords[0]
            x = tupleCoords[0]
            xp = tupleCoords[0]
            y = tupleCoords[1]
            yp = tupleCoords[1]
            horVer = v[len(v) - 1]
            isHorizontal = (horVer == "h")

            if len(val) == variables[v] and self.checkIfValid(variables, tiles, matrixValues, x, y, variables[v],
                                                              isHorizontal, domains, v, val):
                newDomain = deepcopy(domains)
                newDomain[v] = [val]

                for i in range(0, len(val)):
                    matrixValues[xp][yp] = val[i]
                    if isHorizontal:
                        yp = yp + 1
                    else:
                        xp = xp + 1

                startingDomen = deepcopy(newDomain)
                startingMatrixValues = deepcopy(matrixValues)

                for variable in variables:
                    if variable != v:
                        domenToChange = deepcopy(newDomain)
                        if self.updateDomain(domenToChange, variable, matrixValues, variables, tiles):
                            newDomain = deepcopy(domenToChange)
                        else:
                            newDomain = deepcopy(domenToChange)
                            matrixValues = deepcopy(startingMatrixValues)
                            flag = True
                            break

                if flag:
                    solution.append([v, newDomain[v].index(val), newDomain])
                    solution.append([v, None, newDomain])
                    matrixValues = deepcopy(startingMatrixValues)
                    newDomain = deepcopy(startingDomen)
                    continue

                solution.append([v, newDomain[v].index(val), newDomain])
                if self.forwardCheckingIteration(iterationNumber + 1, solution, newDomain, variables,
                                                 deepcopy(matrixValues), tiles):
                    return True

        solution.append([v, None, domains])
        return False

    def getVarCoordinates(self, variable, var_len, tiles):
        _i, _j = int(variable[:-1]) // len(tiles[0]), int(variable[:-1]) % len(tiles[0])
        return zip(range(_i, var_len + _i), [_j] * var_len) \
            if variable[-1] != 'h' \
            else zip([_i] * var_len, range(_j, var_len + _j))

    def checkIfValid(self, variables, tiles, matrixValues, x, y, length, isHorisontal, domains, currV, val):
        newMatrix = deepcopy(matrixValues)
        xp = x
        yp = y

        for i in range(0, len(val)):
            newMatrix[xp][yp] = val[i]
            if (isHorisontal):
                yp = yp + 1
            else:
                xp = xp + 1

        for v in variables:
            if v == currV:
                break
            coordsVar = list(self.getVarCoordinates(v, variables[v], tiles))
            tupleCoordsVar = coordsVar[0]
            xvar = tupleCoordsVar[0]
            yvar = tupleCoordsVar[1]
            horVerVar = v[len(v) - 1]
            isHorisontalVar = (horVerVar == "h")
            lengthVar = variables[v]

            xpVar = xvar
            ypVar = yvar

            for i in range(0, lengthVar):
                if newMatrix[xpVar][ypVar] != matrixValues[xpVar][ypVar]:
                    return False
                if (isHorisontalVar):
                    ypVar = ypVar + 1
                else:
                    xpVar = xpVar + 1

        return True

    def updateDomain(self, domainToChange, variable, matrixValues, variables, tiles):
        newMatrix = deepcopy(matrixValues)
        newDomainToChange = domainToChange[variable]
        newDomainToChangeCopy = deepcopy(newDomainToChange)

        coords = list(self.getVarCoordinates(variable, variables[variable], tiles))
        tupleCoords = coords[0]
        x = tupleCoords[0]
        xp = tupleCoords[0]
        y = tupleCoords[1]
        yp = tupleCoords[1]
        horVer = variable[len(variable) - 1]
        isHorisontal = (horVer == "h")

        for val in newDomainToChange:
            xp = x
            yp = y

            for i in range(0, len(val)):
                newMatrix[xp][yp] = val[i]
                if (isHorisontal):
                    yp = yp + 1
                else:
                    xp = xp + 1

            xp = x
            yp = y
            for i in range(0, len(val)):
                if matrixValues[xp][yp] != 0 and (matrixValues[xp][yp] != newMatrix[xp][yp]):
                    newDomainToChangeCopy.remove(val)
                    break
                if (isHorisontal):
                    yp = yp + 1
                else:
                    xp = xp + 1

        domainToChange[variable] = newDomainToChangeCopy

        if len(domainToChange[variable]) == 0:
            return False
        else:
            return True


class ArcConsistency(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        solution = []
        iterationNumber = 0
        matrixValues = deepcopy(tiles)

        for i in range(len(matrixValues)):
            for j in range(len(matrixValues[0])):
                matrixValues[i][j] = 0

        domains = {var: [word for word in words] for var in variables}

        for var in variables:
            numberOfLetters = variables[var]
            startingDomainVar = []
            for word in domains[var]:
                if len(word) == numberOfLetters:
                    startingDomainVar.append(word)

            domains[var] = startingDomainVar

        self.arcConsistencyIteration(iterationNumber, solution, domains, variables, matrixValues, tiles)

        return solution

    def arcConsistencyIteration(self, iterationNumber, solution, domains, variables, matrixValues, tiles):

        if len(variables) == iterationNumber:
            return True

        v = list(variables.keys())[iterationNumber]

        currentDomain = domains[v]

        for val in domains[v]:
            flag = False
            coords = list(self.getVarCoordinates(v, variables[v], tiles))
            tupleCoords = coords[0]
            x = tupleCoords[0]
            xp = tupleCoords[0]
            y = tupleCoords[1]
            yp = tupleCoords[1]
            horVer = v[len(v) - 1]
            isHorisontal = (horVer == "h")

            if len(val) == variables[v] and self.checkIfValid(variables, tiles, matrixValues, x, y, variables[v],
                                                              isHorisontal, domains, v, val):
                newDomain = deepcopy(domains)
                newDomain[v] = [val]

                for i in range(0, len(val)):
                    matrixValues[xp][yp] = val[i]
                    if (isHorisontal):
                        yp = yp + 1
                    else:
                        xp = xp + 1

                startingDomen = deepcopy(newDomain)

                for variable in variables:
                    if variable != v:
                        domenToChange = deepcopy(newDomain)
                        if (self.updateDomain(domenToChange, variable, matrixValues, variables, tiles)):
                            newDomain = deepcopy(domenToChange)
                        else:
                            newDomain = deepcopy(domenToChange)
                            flag = True
                            break

                if flag:
                    solution.append([v, newDomain[v].index(val), newDomain])
                    solution.append([v, None, newDomain])
                    newDomain = deepcopy(startingDomen)
                    continue

                if not self.arcConsistencyDomainResolving(variables, tiles, newDomain, matrixValues, v,
                                                          iterationNumber):
                    solution.append([v, newDomain[v].index(val), newDomain])
                    solution.append([v, None, newDomain])
                    continue

                solution.append([v, newDomain[v].index(val), newDomain])
                if self.arcConsistencyIteration(iterationNumber + 1, solution, newDomain, variables,
                                                deepcopy(matrixValues), tiles):
                    return True

        solution.append([v, None, domains])
        return False

    def getVarCoordinates(self, variable, var_len, tiles):
        _i, _j = int(variable[:-1]) // len(tiles[0]), int(variable[:-1]) % len(tiles[0])
        return zip(range(_i, var_len + _i), [_j] * var_len) \
            if variable[-1] != 'h' \
            else zip([_i] * var_len, range(_j, var_len + _j))

    def checkIfValid(self, variables, tiles, matrixValues, x, y, length, isHorisontal, domains, currV, val):
        newMatrix = deepcopy(matrixValues)
        xp = x
        yp = y

        for i in range(0, len(val)):
            newMatrix[xp][yp] = val[i]
            if (isHorisontal):
                yp = yp + 1
            else:
                xp = xp + 1

        for v in variables:
            if v == currV:
                break
            coordsVar = list(self.getVarCoordinates(v, variables[v], tiles))
            tupleCoordsVar = coordsVar[0]
            xvar = tupleCoordsVar[0]
            yvar = tupleCoordsVar[1]
            horVerVar = v[len(v) - 1]
            isHorisontalVar = (horVerVar == "h")
            lengthVar = variables[v]

            xpVar = xvar
            ypVar = yvar

            for i in range(0, lengthVar):
                if newMatrix[xpVar][ypVar] != matrixValues[xpVar][ypVar]:
                    return False
                if (isHorisontalVar):
                    ypVar = ypVar + 1
                else:
                    xpVar = xpVar + 1

        return True

    def updateDomain(self, domainToChange, variable, matrixValues, variables, tiles):
        newMatrix = deepcopy(matrixValues)
        newDomainToChange = domainToChange[variable]
        newDomainToChangeCopy = deepcopy(newDomainToChange)

        coords = list(self.getVarCoordinates(variable, variables[variable], tiles))
        tupleCoords = coords[0]
        x = tupleCoords[0]
        xp = tupleCoords[0]
        y = tupleCoords[1]
        yp = tupleCoords[1]
        horVer = variable[len(variable) - 1]
        isHorisontal = (horVer == "h")

        for val in newDomainToChange:
            xp = x
            yp = y

            for i in range(0, len(val)):
                newMatrix[xp][yp] = val[i]
                if (isHorisontal):
                    yp = yp + 1
                else:
                    xp = xp + 1

            xp = x
            yp = y
            for i in range(0, len(val)):
                if matrixValues[xp][yp] != 0 and (matrixValues[xp][yp] != newMatrix[xp][yp]):
                    newDomainToChangeCopy.remove(val)
                    break
                if (isHorisontal):
                    yp = yp + 1
                else:
                    xp = xp + 1

        domainToChange[variable] = newDomainToChangeCopy

        if len(domainToChange[variable]) == 0:
            return False
        else:
            return True

    def arcConsistencyDomainResolving(self, variables, tiles, domains, matrixValues, v, iterationNumber):
        arcList = self.getAllArcs(variables, domains, v, iterationNumber)
        isValid = True

        allUnresolvedVariables = []
        for i in range(0, len(variables)):
            if (i > iterationNumber):
                allUnresolvedVariables.append(list(variables.keys())[i])

        while arcList:
            x, y = arcList.pop(0)
            xValuesToDelete = []
            for valueX in domains[x]:
                yNoValues = True
                for valueY in domains[y]:
                    if self.isValidConstraint(valueX, valueY, x, y, matrixValues, variables, tiles):
                        yNoValues = False
                        break
                if yNoValues:
                    xValuesToDelete.append(valueX)
            if xValuesToDelete:
                domains[x] = [v for v in domains[x] if v not in xValuesToDelete]
                if not domains[x]:
                    isValid = False
                for v in variables:
                    if v != x and v in allUnresolvedVariables:
                        arcList.append((v, x))
        return isValid

    def getAllArcs(self, variables, domains, v, iterationNumber):
        allUnresolvedVariables = []
        for i in range(0, len(variables)):
            if (i > iterationNumber):
                allUnresolvedVariables.append(list(variables.keys())[i])

        listOfArcs = []
        for i in range(0, len(variables)):
            for j in range(0, len(variables)):
                if i != j:
                    if list(variables.keys())[i] in allUnresolvedVariables and list(variables.keys())[
                        j] in allUnresolvedVariables:
                        listOfArcs.append((list(variables.keys())[i], list(variables.keys())[j]))

        return listOfArcs

    def isValidConstraint(self, val_x, val_y, xVar, yVar, matrixValues, variables, tiles):
        newMatrix = deepcopy(matrixValues)

        for i in range(len(newMatrix)):
            for j in range(len(newMatrix[0])):
                newMatrix[i][j] = 0

        coordsXVar = list(self.getVarCoordinates(xVar, variables[xVar], tiles))
        tupleCoordsXVar = coordsXVar[0]
        xXVar = tupleCoordsXVar[0]
        xpXVar = tupleCoordsXVar[0]
        yXVar = tupleCoordsXVar[1]
        ypXVar = tupleCoordsXVar[1]
        horVerXVar = xVar[len(xVar) - 1]
        isHorisontalXVar = (horVerXVar == "h")

        coordsYVar = list(self.getVarCoordinates(yVar, variables[yVar], tiles))
        tupleCoordsYVar = coordsYVar[0]
        xYVar = tupleCoordsYVar[0]
        xpYVar = tupleCoordsYVar[0]
        yYVar = tupleCoordsYVar[1]
        ypYVar = tupleCoordsYVar[1]
        horVerYVar = yVar[len(yVar) - 1]
        isHorisontalYVar = (horVerYVar == "h")

        xpXVar = xXVar
        ypXVar = yXVar

        for i in range(0, len(val_x)):
            newMatrix[xpXVar][ypXVar] = val_x[i]
            if (isHorisontalXVar):
                ypXVar = ypXVar + 1
            else:
                xpXVar = xpXVar + 1

        xpYVar = xYVar
        ypYVar = yYVar

        for i in range(0, len(val_y)):
            if newMatrix[xpYVar][ypYVar] != 0 and (val_y[i] != newMatrix[xpYVar][ypYVar]):
                return False
            if (isHorisontalYVar):
                ypYVar = ypYVar + 1
            else:
                xpYVar = xpYVar + 1

        return True

    def areVariablesConstrained(self, vVar, xVar, variables, tiles):
        coordsXVar = list(self.getVarCoordinates(xVar, variables[xVar], tiles))
        tupleCoordsXVar = coordsXVar[0]
        xXVar = tupleCoordsXVar[0]
        xpXVar = tupleCoordsXVar[0]
        yXVar = tupleCoordsXVar[1]
        ypXVar = tupleCoordsXVar[1]
        horVerXVar = xVar[len(xVar) - 1]
        isHorisontalXVar = (horVerXVar == "h")

        coordsVVar = list(self.getVarCoordinates(vVar, variables[vVar], tiles))
        tupleCoordsVVar = coordsVVar[0]
        xVVar = tupleCoordsVVar[0]
        xpVVar = tupleCoordsVVar[0]
        yVVar = tupleCoordsVVar[1]
        ypVVar = tupleCoordsVVar[1]
        horVerVVar = vVar[len(vVar) - 1]
        isHorisontalVVar = (horVerVVar == "h")

        return True
