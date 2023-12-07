package main

import (
	"fmt"
	"math/rand"
	"time"
)

// distribuição triangular
type Triangular struct {
	Min  float64
	Mode float64
	Max  float64
}

// gera um valor aleatório de acordo com a distribuição triangular
func (t *Triangular) Rand() float64 {
	r := rand.Float64()
	if r <= (t.Mode-t.Min)/(t.Max-t.Min) {
		return t.Min + (t.Max-t.Min)*r
	}
	return t.Max - (t.Max-t.Min)*(1-r)
}

// define o sistema de controle fuzzy
type SistemaFuzzy struct {
	Angle                float64
	AngularVelocity      float64
	Output               float64
	AngleLeft            *Triangular
	AngleVertical        *Triangular
	AngleRight           *Triangular
	AngularVelocityLeft  *Triangular
	AngularVelocityZero  *Triangular
	AngularVelocityRight *Triangular
	OutputNegative       *Triangular
	OutputZero           *Triangular
	OutputPositive       *Triangular
}

// inicializa o sistema de controle fuzzy
func InicializarSistemaFuzzy() *SistemaFuzzy {
	angleLeft := Triangular{Min: -90, Mode: -90, Max: 0}
	angleVertical := Triangular{Min: -45, Mode: 0, Max: 45}
	angleRight := Triangular{Min: 0, Mode: 90, Max: 90}

	angularVelocityLeft := Triangular{Min: -10, Mode: -10, Max: 0}
	angularVelocityZero := Triangular{Min: -5, Mode: 0, Max: 5}
	angularVelocityRight := Triangular{Min: 0, Mode: 10, Max: 10}

	outputNegative := Triangular{Min: -1, Mode: -1, Max: 0}
	outputZero := Triangular{Min: -1, Mode: 0, Max: 1}
	outputPositive := Triangular{Min: 0, Mode: 1, Max: 1}

	return &SistemaFuzzy{
		AngleLeft:            &angleLeft,
		AngleVertical:        &angleVertical,
		AngleRight:           &angleRight,
		AngularVelocityLeft:  &angularVelocityLeft,
		AngularVelocityZero:  &angularVelocityZero,
		AngularVelocityRight: &angularVelocityRight,
		OutputNegative:       &outputNegative,
		OutputZero:           &outputZero,
		OutputPositive:       &outputPositive,
	}
}

// avalia o sistema fuzzy com regras e parametros dados
func AvaliarSistemaFuzzy(sistema *SistemaFuzzy, regras []int) float64 {
	antecedentIndex := regras[0]
	consequentIndex := regras[1]
	outputIndex := regras[2]

	switch antecedentIndex {
	case 0:
		sistema.AngleLeft.Rand()
	case 1:
		sistema.AngleVertical.Rand()
	case 2:
		sistema.AngleRight.Rand()
	}

	switch consequentIndex {
	case 0:
		sistema.AngularVelocityLeft.Rand()
	case 1:
		sistema.AngularVelocityZero.Rand()
	case 2:
		sistema.AngularVelocityRight.Rand()
	}

	switch outputIndex {
	case 0:
		sistema.Output = sistema.OutputNegative.Rand()
	case 1:
		sistema.Output = sistema.OutputZero.Rand()
	case 2:
		sistema.Output = sistema.OutputPositive.Rand()
	}

	return sistema.Output
}

// avalia a qualidade de um individuo
func FuncaoFitness(regras []int) float64 {
	sistema := InicializarSistemaFuzzy()
	sistema.Angle = -30
	sistema.AngularVelocity = -5

	return AvaliarSistemaFuzzy(sistema, regras)
}

// otimiza o sistema fuzzy utilizando algoritmo genetico
func Genetico(populationSize, numGenerations int) []int {
	rand.Seed(time.Now().UnixNano())

	// população inicial
	population := make([][]int, populationSize)
	for i := range population {
		population[i] = make([]int, 3)
		for j := range population[i] {
			population[i][j] = rand.Intn(3)
		}
	}

	// avaliação da população inicial
	scores := make([]float64, populationSize)
	for i, individual := range population {
		scores[i] = FuncaoFitness(individual)
	}

	// algoritmo genetico
	var bestIndividual []int
	bestScore := -1.0

	for gen := 0; gen < numGenerations; gen++ {
		// calculo de crossover
		for i := 0; i < populationSize; i += 2 {
			crossoverPoint := rand.Intn(3)
			for j := 0; j < crossoverPoint; j++ {
				population[i][j], population[i+1][j] = population[i+1][j], population[i][j]
			}
		}

		// calculo de mutação
		for i := 0; i < populationSize; i++ {
			mutationPoint := rand.Intn(3)
			population[i][mutationPoint] = rand.Intn(3)
		}

		// avaliação da população após crossover e mutação
		for i, individual := range population {
			scores[i] = FuncaoFitness(individual)
		}

		// seleção do melhor individuo
		for i, score := range scores {
			if score > bestScore {
				bestIndividual = make([]int, 3)
				copy(bestIndividual, population[i])
				bestScore = score
			}
		}
	}

	return bestIndividual
}

func main() {
	bestIndividual := Genetico(10, 5)

	sistema := InicializarSistemaFuzzy()
	sistema.Angle = -30
	sistema.AngularVelocity = -5

	resultado := AvaliarSistemaFuzzy(sistema, bestIndividual)

	fmt.Printf("Sistema FIS otimizado: %v\n", resultado)
}
